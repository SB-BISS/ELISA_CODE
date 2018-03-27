# Transcribe audio to text ------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# First we need to convert the object to wav file
# ~~~~~~~~~~~~~~~~~~~~
# install.packages("tuneR")
library(tuneR) 
test_audio <- "Elisa/Nokia/Nokia Q1-2012.mp3"
mp3_file <- readMP3(test_audio)
WAV_DIR <- "Elisa"
writeWave(mp3_file, paste0(WAV_DIR, "/wav_file.wav"), extensible = F) # write the mp3 to wav
file.info(paste0(WAV_DIR, "/wav_file.wav"))$size # get the size of the file
# Done converting to wav file

# ~~~~~~~~~~~~~~~~~~~~
# Upload to cloud
# ~~~~~~~~~~~~~~~~~~~~
# install.packages("googleCloudStorageR")
library(googleCloudStorageR)
gl_auth(json_file) # we need to authenticate
buckets <- gcs_list_buckets(projectId= "march-197214")
# Let's upload our file
gcs_upload(file= "Elisa/wav_file.wav", bucket= buckets$name[[1]], name = "wav_file.wav")
audio_file <- "gs://18-march-bucket/wav_file.wav"

transcript0 <- gl_speech(test_audio, asynch = TRUE, sampleRateHertz= 11025)  # sampleRateHertz is important info, you get by right-click on the file itself
transcript <- gl_speech_op(transcript0) # Wait some time and re-run that line
class(transcript)
names(transcript)
