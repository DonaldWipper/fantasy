git add .
git commit -m $1
echo $1
git push https://$2:$3@github.com/$2/$4 --all 
