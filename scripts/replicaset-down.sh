port=40000

for i in 0 1 2
do
  mongo <./shutdown.js --port $(($port + $i))
done
