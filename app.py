from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import sys

# Load environment variables
load_dotenv()

def parse_markdown_file(file_path):
    """Read markdown file and separate settings from content"""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            
        # Split the content at '### content'
        parts = content.split('### content')
        if len(parts) != 2:
            raise ValueError("File must contain '### content' section")
            
        # Get the settings part
        settings_part = parts[0].split('### settings')[1].strip()
        
        # Parse settings
        settings = {}
        for line in settings_part.split('\n'):
            if line.strip() and ':' in line:
                key, value = line.split(':', 1)
                settings[key.strip()] = value.strip()
                
        # Convert settings to appropriate types
        settings = {
            'voice_id': settings.get('voice_id', 'YgjXqgzBJa9op0K278OW'),
            'model': settings.get('model', 'eleven_multilingual_v2'),
            'stability': float(settings.get('stability', 1.0)),
            'similarity_boost': float(settings.get('similarity_boost', 0.60)),
            'style': float(settings.get('style', 0.37)),
            'speaker_boost': settings.get('speaker_boost', 'true').lower() == 'true'
        }
        
        # Get the content part
        text_content = parts[1].strip()
        
        return settings, text_content
            
    except Exception as e:
        print(f"❌ Error parsing markdown file: {str(e)}")
        return None, None

def generate_speech(text, settings, output_filename=None):
    try:
        # API Configuration
        api_key = os.getenv('ELEVENLABS_API_KEY')
        voice_id = settings['voice_id']
        
        # API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        # Headers
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        # Request body
        body = {
            "text": text,
            "model_id": settings['model'],
            "voice_settings": {
                "stability": settings['stability'],
                "similarity_boost": settings['similarity_boost'],
                "style": settings['style'],
                "use_speaker_boost": settings['speaker_boost']
            }
        }
        
        # Make request
        print("🎤 Generating speech with settings:")
        print(f"   Voice ID: {settings['voice_id']}")
        print(f"   Model: {settings['model']}")
        print(f"   Stability: {settings['stability']}")
        print(f"   Similarity Boost: {settings['similarity_boost']}")
        print(f"   Style: {settings['style']}")
        print(f"   Speaker Boost: {settings['speaker_boost']}")
        
        response = requests.post(url, json=body, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Create output directory if it doesn't exist
            if not os.path.exists("output"):
                os.makedirs("output")
                
            # Generate filename if not provided
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"output/speech_{timestamp}.mp3"
            
            # Save the audio file
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Audio saved successfully as: {output_filename}")
            return output_filename
        else:
            print(f"❌ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error generating speech: {str(e)}")
        return None

def process_markdown_file(input_file):
    # Read the markdown content and settings
    settings, text = parse_markdown_file(input_file)
    if text is None or settings is None:
        return
    
    # Create output filename based on input filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"output/{base_name}.mp3"
    
    # Generate speech
    print(f"🎯 Processing {input_file}...")
    generate_speech(text, settings, output_filename)

def main():
    if len(sys.argv) > 1:
        # If file path is provided as argument
        input_file = sys.argv[1]
        if not os.path.exists(input_file):
            print(f"❌ Error: File {input_file} not found")
            return
        process_markdown_file(input_file)
    else:
        print("❌ Please provide a markdown file path")
        print("Usage: ./convert.sh your-file.md")

if __name__ == "__main__":
    main()