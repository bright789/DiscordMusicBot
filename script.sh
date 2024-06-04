# Install Git LFS
git lfs install

# Track the large files with Git LFS
git lfs track "ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
git lfs track "ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe"
git lfs track "ffmpeg-master-latest-win64-gpl/bin/ffplay.exe"

# Add .gitattributes to the repository
git add .gitattributes

# Add all files to the staging area
git add .

# Commit the changes
git commit -m "Track large files with Git LFS"

# Push the changes to the remote repository
git push origin master
