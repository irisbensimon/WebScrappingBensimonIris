curl https://fr.investing.com/equities/l.v.m.h. > LVMH.html
current_date=$(date +"%Y-%m-%d %T")
latest_price=$(cat LVMH.html | grep -oP '(?<=<div class=\"text-5xl font-bold leading-9 md:text-\[42px\] md:leading-\[60px\] text-\[#232526\]\">)[^<]+' | tr ',' '.' )
echo "$current_date,$latest_price" >> cours_action.csv

