cd /home/ec2-user/Project/WebScrappingBensimonIris
curl https://www.tradingsat.com/lvmh-FR0000121014/actualites.html > LVMH.html
current_date=$(date +"%Y-%m-%d %T")
latest_price=$(cat LVMH.html | grep -oP '(?<=<span class=\"price\">)[^ ]+' | tr ',' '.' )
echo "$current_date,$latest_price" >> cours_action.csv

