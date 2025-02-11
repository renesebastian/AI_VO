# LBL_VOLABS

A Docker-based text-to-speech conversion tool using ElevenLabs API.

## Prerequisites

- Docker Desktop installed on your machine
- ElevenLabs API key ([Get it here](https://elevenlabs.io/))

## First Time Setup

1. Clone this repository to your local machine

2. Create required directories:
```bash
mkdir input output
```

3. Create and set up your environment file:
```bash
echo "ELEVENLABS_API_KEY=your_api_key_here" > .env
```
Replace `your_api_key_here` with your actual ElevenLabs API key.

4. Build the Docker container:
```bash
docker build --no-cache -t lbl-volabs .
```

5. Create a template file in the input directory:
```markdown
### settings
voice_id: YgjXqgzBJa9op0K278OW
model: eleven_multilingual_v2
stability: 1.0
similarity_boost: 0.60
style: 0.37
speaker_boost: true

### content
Enter your text here...
```
Save this as `input/template.md`

## Usage

1. Create a new markdown file in the `input` directory:
   - Copy `template.md` to create a new file
   - Or create a new file following the same format
   - Add your content under the `### content` section

2. Convert text to speech:
```bash
./convert.sh yourfile.md
```
Replace `yourfile.md` with your markdown filename.

3. Find the generated audio file in the `output` directory

## File Structure

```
LBL_VOLABS/
├── .env                # API key configuration
├── .gitignore         # Git ignore file
├── Dockerfile         # Docker configuration
├── app.py            # Main application code
├── convert.sh        # Conversion script
├── requirements.txt  # Python dependencies
├── input/           # Input markdown files
│   └── template.md   # Template file
└── output/          # Generated audio files
```

## Tips

- Always copy `template.md` when creating new files to ensure correct formatting
- The script automatically looks in the `input` directory, so you only need to provide the filename
- Check the terminal output for any errors or success messages
- Generated audio files will have the same name as your input file (with .mp3 extension)

## Settings Explanation

In your markdown files, you can adjust these settings:

- `voice_id`: Your ElevenLabs voice ID
- `model`: The model to use (e.g., `eleven_multilingual_v2`)
- `stability`: Voice stability (0.0 to 1.0)
- `similarity_boost`: Voice similarity boost (0.0 to 1.0)
- `style`: Voice style (0.0 to 1.0)
- `speaker_boost`: Enhanced voice clarity (true/false)

## Troubleshooting

If you encounter issues:

1. Verify your API key in the `.env` file
2. Check that your markdown file follows the correct format
3. Ensure Docker Desktop is running
4. Try rebuilding the Docker container:
   ```bash
   docker build --no-cache -t lbl-volabs .
   ```