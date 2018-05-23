curl -X POST -u 56920326-be84-43e0-ade4-9744285f5a13:RTd7WB53NToT \
--header "Content-Type: audio/flac" \
--data-binary @./audio-file.flac  \
"https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
