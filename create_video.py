import cv2
import numpy as np
import math
import random

def create_video(messages, filename):
    # Video settings
    width = 640
    height = 480
    fps = 30
    duration = 15  # seconds
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    # Create frames
    for i in range(fps * duration):
        # Create a dark casino-themed background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add animated background with casino-style pattern
        time_factor = i / fps
        for x in range(0, width, 20):
            for y in range(0, height, 20):
                # Create subtle pulsing effect
                pulse = (math.sin(time_factor * 2 + x/200 + y/200) + 1) * 15
                color = (int(50 + pulse), int(50 + pulse), int(50 + pulse))
                cv2.rectangle(frame, (x, y), (x + 20, y + 20), color, 1)
        
        # Add casino-style text
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Different messages based on time
        time_segment = i / (fps * duration)
        segment_index = int(time_segment * len(messages))
        if segment_index >= len(messages):
            segment_index = len(messages) - 1
            
        main_text, sub_text = messages[segment_index]
        
        # Calculate text positions
        main_size = cv2.getTextSize(main_text, font, 2.5, 3)[0]
        sub_size = cv2.getTextSize(sub_text, font, 1.5, 3)[0]
        
        main_x = (width - main_size[0]) // 2
        main_y = (height - main_size[1]) // 2 - 40
        sub_x = (width - sub_size[0]) // 2
        sub_y = (height + sub_size[1]) // 2 + 20
        
        # Add gold gradient effect to text
        for offset in range(4, 0, -1):
            # Gold color with varying intensity
            gold_color = (0, int(215 - offset*30), int(255 - offset*30))
            cv2.putText(frame, main_text, (main_x-offset, main_y-offset), font, 2.5, gold_color, 3)
            cv2.putText(frame, sub_text, (sub_x-offset, sub_y-offset), font, 1.5, gold_color, 3)
        
        # Add main text
        cv2.putText(frame, main_text, (main_x, main_y), font, 2.5, (0, 215, 255), 3)
        cv2.putText(frame, sub_text, (sub_x, sub_y), font, 1.5, (0, 215, 255), 3)
        
        # Add decorative elements
        # Top border with animated width
        border_width = int(width * 0.8 * (0.5 + 0.5 * math.sin(time_factor * 3)))
        cv2.line(frame, 
                ((width - border_width)//2, 50), 
                ((width + border_width)//2, 50), 
                (0, 215, 255), 3)
        
        # Bottom border with animated width
        cv2.line(frame, 
                ((width - border_width)//2, height-50), 
                ((width + border_width)//2, height-50), 
                (0, 215, 255), 3)
        
        # Add animated progress bar
        progress = i / (fps * duration)
        bar_width = int(width * 0.8)
        bar_height = 25
        bar_x = (width - bar_width) // 2
        bar_y = height - 70
        
        # Draw bar background with gold tint
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (0, 100, 150), -1)
        
        # Draw animated progress
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            # Add pulsing effect to progress bar
            pulse = (math.sin(time_factor * 5) + 1) * 30
            bar_color = (0, int(215 + pulse), int(255 + pulse))
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), bar_color, -1)
            
            # Add motivational text
            loading_text = "YOUR NEXT BIG WIN AWAITS..."
            loading_size = cv2.getTextSize(loading_text, font, 0.8, 2)[0]
            loading_x = (width - loading_size[0]) // 2
            loading_y = bar_y - 15
            cv2.putText(frame, loading_text, (loading_x, loading_y), font, 0.8, (0, 215, 255), 2)
        
        # Add sparkle effects
        if i % 5 == 0:  # More frequent sparkles
            for _ in range(3):  # Multiple sparkles per frame
                sparkle_x = random.randint(0, width)
                sparkle_y = random.randint(0, height)
                size = random.randint(2, 4)
                cv2.circle(frame, (sparkle_x, sparkle_y), size, (0, 215, 255), -1)
        
        # Write frame
        out.write(frame)
    
    # Release video writer
    out.release()
    print(f"Video {filename} created successfully!")

def create_all_videos():
    # Video 1: Classic Gambling Propaganda
    messages1 = [
        ("WIN BIG", "OR GO HOME"),
        ("99% QUIT", "BEFORE WINNING BIG"),
        ("YOUR LUCKY", "STREAK IS COMING")
    ]
    create_video(messages1, "video1.mp4")
    
    # Video 2: High Stakes Theme
    messages2 = [
        ("HIGH STAKES", "HIGH REWARDS"),
        ("PLAY LIKE A PRO", "WIN LIKE A KING"),
        ("FORTUNE FAVORS", "THE BOLD")
    ]
    create_video(messages2, "video2.mp4")
    
    # Video 3: Lucky Streak Theme
    messages3 = [
        ("LUCKY STREAK", "INCOMING"),
        ("JUST ONE MORE", "BIG WIN"),
        ("YOUR TIME", "IS NOW")
    ]
    create_video(messages3, "video3.mp4")
    
    # Video 4: Persistence Theme
    messages4 = [
        ("DON'T QUIT", "WHEN YOU'RE DOWN"),
        ("COMEBACKS", "ARE REAL"),
        ("NEXT HAND", "COULD BE IT")
    ]
    create_video(messages4, "video4.mp4")
    
    # Video 5: VIP Theme
    messages5 = [
        ("PLAY LIKE", "A VIP"),
        ("WIN LIKE", "A LEGEND"),
        ("YOUR MOMENT", "OF GLORY")
    ]
    create_video(messages5, "video5.mp4")

if __name__ == "__main__":
    create_all_videos() 