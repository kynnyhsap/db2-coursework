rs.initiate()

// add secondary nodes
const PORT = 40000
rs.add("localhost:" + (PORT + 1))
rs.add("localhost:" + (PORT + 2))

rs.secondaryOk()


// check status
rs.status()
