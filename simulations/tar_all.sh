dirs=$(find .  -maxdepth 1 -mindepth 1 -type d)
for dir in $dirs
do
  cleaned_dir=$(echo $dir | cut -d "/" -f 2)
  tar_archive=${cleaned_dir}.tar
  if [ ! -f "$tar_archive" ]
  then
    echo Taring $cleaned_dir to $tar_archive
    tar hcf $tar_archive $cleaned_dir
    tar --compare --file=$tar_archive
  fi
done
