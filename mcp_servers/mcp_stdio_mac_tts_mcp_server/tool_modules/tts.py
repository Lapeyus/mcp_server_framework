import subprocess
import shlex
import os
from typing import Optional

def text_to_speech_mac(text_to_speak: str, voice: Optional[str] = None, output_file_path: Optional[str] = None) -> dict:
    """
    Converts text to speech using the macOS 'say' command.

    Args:
        text_to_speak (str): The text to be spoken or saved to an audio file.
        voice (str, optional): The voice to use (e.g., "Alex", "Victoria"). 
                               If None, the system's default voice is used.
        output_file_path (str, optional): 
            If provided, the audio will be saved to this file path.
            The file extension should typically be .aiff, .m4a, or .wav.
            Example: "output_audio.aiff".
            If None, the text will be spoken directly.

    Returns:
        dict: A dictionary containing the status of the operation.
              Example success (spoken): 
                {"status": "success", "message": "Text spoken successfully."}
              Example success (saved to file): 
                {"status": "success", "message": "Audio saved to file.", "file_path": "path/to/output.aiff"}
              Example error: 
                {"status": "error", "error_message": "Description of the error."}
    """
    if not text_to_speak or not text_to_speak.strip():
        return {"status": "error", "error_message": "Input text cannot be empty."}

    try:
        command = ["say"]

        # if voice:
        #     command.extend(["-v", voice]) #

        if output_file_path:
            # Ensure the directory for the output file exists if a path is given
            output_dir = os.path.dirname(output_file_path)
            if output_dir and not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except OSError as e:
                    return {"status": "error", "error_message": f"Could not create directory for output file: {e}"}
            
            # shlex.quote output_file_path to handle spaces or special characters
            command.extend(["-o", shlex.quote(output_file_path)])
        
        # text_to_speak will be passed via stdin
        
        # Join command for logging or debugging, but run as a list for subprocess
        # logging.info(f"Executing TTS command: {' '.join(command)}") # If logging is set up

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Pass text_to_speak via stdin, encoded as UTF-8
        stdout, stderr = process.communicate(input=text_to_speak.encode('utf-8'), timeout=30) # Timeout to prevent hanging

        if process.returncode == 0:
            if output_file_path:
                return {
                    "status": "success", 
                    "message": f"Audio successfully saved to {output_file_path}",
                    "file_path": output_file_path
                }
            else:
                return {"status": "success", "message": "Text spoken successfully."}
        else:
            error_message = stderr.decode().strip() if stderr else "Unknown error during 'say' command execution."
            return {"status": "error", "error_message": error_message, "return_code": process.returncode}

    except FileNotFoundError:
        return {"status": "error", "error_message": "'say' command not found. This function is for macOS only."}
    except subprocess.TimeoutExpired:
        return {"status": "error", "error_message": "'say' command timed out."}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {str(e)}"}

if __name__ == '__main__':
    # Example Usage (for direct testing of this script)
    # Spoken directly
    result1 = text_to_speech_mac("Hello from Python using the say command!")
    print(f"Spoken result: {result1}")

    result_custom_voice = text_to_speech_mac("This is a test with a custom voice.", voice="Alex")
    print(f"Spoken result (Alex): {result_custom_voice}")

    # Saved to file (ensure you have write permissions in the current directory)
    # Using a relative path for the output file
    output_filename = "test_audio.aiff"
    result2 = text_to_speech_mac("This audio is saved to a file.", output_file_path=output_filename)
    print(f"Saved to file result: {result2}")
    if result2["status"] == "success":
        print(f"Audio file created at: {os.path.abspath(output_filename)}")

    # Test with empty text
    result_empty = text_to_speech_mac("")
    print(f"Empty text result: {result_empty}")
    
    # Test with non-existent voice (example, behavior might vary)
    result_bad_voice = text_to_speech_mac("Testing a bad voice.", voice="NonExistentVoice")
    print(f"Bad voice result: {result_bad_voice}")

    # Test saving to a path that might require directory creation
    # Ensure 'temp_audio' directory does not exist or test its creation
    # output_in_subdir = "temp_audio/subdir_test.aiff"
    # result_subdir = text_to_speech_mac("Testing audio in a subdirectory.", output_file_path=output_in_subdir)
    # print(f"Subdirectory save result: {result_subdir}")
    # if result_subdir.get("status") == "success":
    #     print(f"Audio file created at: {os.path.abspath(output_in_subdir)}")
