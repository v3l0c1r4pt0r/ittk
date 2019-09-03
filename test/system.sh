#!/bin/bash
# system tests for itetool.py -u
set -e
if [ $# -lt 1 ]; then
  echo "Usage: $0 parent-of-LKV373A-fw"
  exit 1
fi
dir=$1
files="$(cat <<EOF
LKV373A-fw/IPTV_command_library_and_tool_20160303/TX/IPTV_TX_PKG_v4_0_0_0_20160427.PKG
LKV373A-fw/IPTV_command_library_and_tool_20160303/RX/IPTV_RX_PKG_v0_5_0_0_20160427.PKG
LKV373A-fw/RX firmware - dont flash into TX/LKV373A_RX_20151105_PKG.PKG
LKV373A-fw/RX firmware - dont flash into TX/LKV373A_RX_V3.0b_20160218.PKG
LKV373A-fw/RX firmware - dont flash into TX/LKV373A_RX_20160615.PKG
LKV373A-fw/RX firmware - dont flash into TX/LKV373A_RX_V3.0c_d_20161116_PKG.PKG
LKV373A-fw/RX firmware - dont flash into TX/LKV373A_RX_V3.0_20151130_PKG.PKG
LKV373A-fw/RX firmware - dont flash into TX/RX_V1.3c_20161021_PKG.PKG
LKV373A-fw/TX firmware/LKV373A_TX_V3.0_20151130_PKG.PKG
LKV373A-fw/TX firmware/TX_V1.3c_20161104_PKG.PKG
LKV373A-fw/TX firmware/LKV373A_TX_V3.0c_d_20161116_PKG.PKG
LKV373A-fw/TX firmware/LKV373A_TX_SENDER_20160722.PKG
LKV373A-fw/TX firmware/LKV373A_TX_V3.0b_20160218.PKG
LKV373A-fw/TX firmware/LKV373A_TX_20151028_PKG.PKG
EOF
)"

echo "Going to extract following files. One second to interrupt..."
echo "$files" | while read f; do
  ls -l "$dir/$f"
done
sleep 1

echo "Let the show begin"
echo "$files" | while read f; do
  d="$(basename "$f")"
  rel="$(dirname "$0")"
  echo "$rel"/../itetool.py "$dir/$f" -d"$rel/$d" -u
  "$rel"/../itetool.py "$dir/$f" -d"$rel/$d" -u
done
echo "Done"
