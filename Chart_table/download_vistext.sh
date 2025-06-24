    #!/bin/bash
# Script to download and unzip VisText data files into /mnt/VLAI_data/vistext

function usage {
  echo "Usage: $0 [--images] [--scenegraphs] [--vl_spec]"
  echo "  --images        Download rasterized chart images."
  echo "  --scenegraphs   Download full scenegraphs."
  echo "  --vl_spec       Download Vega-Lite specs."
  exit 1
}

# Default flags
images=false
scenegraphs=false
vl_spec=false

# Parse arguments
while [[ $1 != "" ]]; do
  case $1 in
    --images)        images=true     ;;
    --scenegraphs)   scenegraphs=true;;
    --vl_spec)       vl_spec=true    ;;
    *) usage ;;
  esac
  shift
done

# Base directories
DATA_DIR="/mnt/VLAI_data/vistext/"

mkdir -p "$DATA_DIR"
mkdir -p "$MODELS_DIR"

echo "Downloading tabular data..."
wget -q --show-progress https://vis.csail.mit.edu/vistext/tabular.zip -P "$DATA_DIR"

if $images; then
  echo "Downloading rasterized images..."
  wget -q --show-progress https://vis.csail.mit.edu/vistext/images.zip -P "$DATA_DIR"
fi

if $scenegraphs; then
  echo "Downloading scenegraphs..."
  wget -q --show-progress https://vis.csail.mit.edu/vistext/scenegraphs.zip -P "$DATA_DIR"
fi

if $vl_spec; then
  echo "Downloading Vega-Lite specs..."
  wget -q --show-progress https://vis.csail.mit.edu/vistext/vl_spec.zip -P "$DATA_DIR"
fi

echo "Download complete. Unzipping archives..."

# Unzip all requested files
unzip -o "$DATA_DIR/tabular.zip"        -d "$DATA_DIR"
if $images; then
  unzip -o "$DATA_DIR/images.zip"      -d "$DATA_DIR"
fi
if $scenegraphs; then
  unzip -o "$DATA_DIR/scenegraphs.zip" -d "$DATA_DIR"
fi
if $vl_spec; then
  unzip -o "$DATA_DIR/vl_spec.zip"     -d "$DATA_DIR"
fi

echo "All done. Files are in $DATA_DIR."

# bash download_vistext.sh --images --scenegraphs --vl_spec