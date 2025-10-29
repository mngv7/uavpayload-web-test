import cv2
import socket
import argparse
import os
import time

LOGS_FILE_PATH = "logs/test_logs.txt"

def send_video_udp(host, port, video_path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Could not open {video_path}")
        return
    
    print(f"Streaming {video_path} to {host}:{port}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()

        max_packet_size = 60000
        for i in range(0, len(data), max_packet_size):
            sock.sendto(data[i:i+max_packet_size], (host, port))

    print("Video streaming complete.")
    cap.release()
    sock.close()

def send_logs_tcp(host, port, delay=0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    with open(LOGS_FILE_PATH, "r") as logs_file:
        for line in logs_file:
            line = line.strip()
            encoded_line = line.encode("utf-8")
            length_prefix = len(encoded_line).to_bytes(4, "big")
            sock.sendall(length_prefix)
            sock.sendall(encoded_line)
            if delay > 0:
                time.sleepms(delay)
    sock.close()
    print("Logs sent successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send video or logs to a host")
    parser.add_argument("--type", type=str, required=True, choices=["video", "logs"], help="Type of data to send")
    parser.add_argument("--host", type=str, required=True, help="Destination host IP")
    parser.add_argument("--port", type=int, required=True, help="Destination port")
    parser.add_argument("--video", type=str, default="media/video.mp4", help="Path to video file")
    args = parser.parse_args()

    if args.type == "video":
        if not os.path.exists(args.video):
            print(f"Video file {args.video} does not exist.")
            exit(1)
        send_video_udp(args.host, args.port, args.video)
    elif args.type == "logs":
        if not os.path.exists(LOGS_FILE_PATH):
            print(f"Logs file {LOGS_FILE_PATH} does not exist.")
            exit(1)
        send_logs_tcp(args.host, args.port, 0.5)
