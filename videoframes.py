import cv2
import os

def get_unique_folder(base_name):
    """Checks if folder exists, returns new name (e.g., mango -> mango1 -> mango2)"""
    if not os.path.exists(base_name):
        return base_name
    
    # If exists, ask for action
    print(f"\nFolder '{base_name}' already exists.")
    action = input("Choose action: [o]verwrite, [c]ancel, [n]ew folder (default 'n'): ").lower()
    
    if action == 'o':
        return base_name
    elif action == 'c':
        return None
    else:
        # Generate new name with incrementing number
        counter = 1
        new_name = f"{base_name}{counter}"
        while os.path.exists(new_name):
            counter += 1
            new_name = f"{base_name}{counter}"
        return new_name

def main():
    print("--- Video Frame Extractor ---")
    video_path = input("Enter the path to your video file: ").strip('"')
    
    if not os.path.exists(video_path):
        print(f"Error: '{video_path}' was not found.")
        input("\nPress Enter to close...")
        return

    # Determine folder name using our new function
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_folder = get_unique_folder(base_name)
    
    if output_folder is None:
        print("Operation cancelled.")
        input("\nPress Enter to close...")
        return
        
    os.makedirs(output_folder, exist_ok=True)

    # Frame extraction setup
    vidcap = cv2.VideoCapture(video_path)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    max_input = input(f"Enter max frames to extract (Total: {total_frames}, default:ALL): ")
    limit = int(max_input) if max_input.strip() else total_frames

    print(f"\nExtracting {limit} frames into '{output_folder}/'...")

    count = 0
    while count < limit:
        success, image = vidcap.read()
        if not success:
            break
            
        frame_filename = os.path.join(output_folder, f"frame_{count:05d}.jpg")
        cv2.imwrite(frame_filename, image)
        count += 1
        
        if count % 50 == 0:
            print(f"Progress: {((count / limit) * 100):.1f}%")

    vidcap.release()
    print(f"\n{count} frames saved in '{output_folder}'.")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()