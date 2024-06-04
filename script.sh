#!/bin/bash

# Remove the large files from Git history
git rm --cached ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe
git rm --cached ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe
git rm --cached ffmpeg-master-latest-win64-gpl/bin/ffplay.exe

# Clean up Git history to remove large files
pip install git-filter-repo
git filter-repo --strip-blobs-bigger-than 100M

# Track the large files with Git LFS
git lfs track "ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
git lfs track "ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe"
git lfs track "ffmpeg-master-latest-win64-gpl/bin/ffplay.exe"

# Add the .gitattributes file
git add .gitattributes

# Re-add the large files so they are tracked by Git LFS
git add ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe
git add ffmpeg-master-latest-win64-gpl/bin/ffprobe.exe
git add ffmpeg-master-latest-win64-gpl/bin/ffplay.exe

# Commit the changes
git commit -m "Track large files with Git LFS"

# Push the changes to GitHub
git push origin master
