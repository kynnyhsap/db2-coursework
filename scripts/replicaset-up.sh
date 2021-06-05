volumes=../data/volumes
set=rs
port=40000
default_color=$(tput sgr0)

for i in 0 1 2
do
  mkdir -p $volumes/$set-$i
done

# run mongodb servers
for i in 0 1 2
do
  mongod --replSet "$set" --dbpath $volumes/$set-$i --port $(($port + $i)) --bind_ip localhost \
    | sed "s/.*/$(tput setaf $((i+1)))&$default_color/" & # this line is for color output, DON'T TOUCH IT
done

# wait a bit for the first server to come up
sleep 10

# initiate replica set
mongo <./rs-init.js --port $port

# sleep forever
cat