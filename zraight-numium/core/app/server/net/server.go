package net

import (
	"fmt"
	"net"
)

type Server struct {
	host string
	port int
}

func handleConnection(conn net.Conn) {
	defer conn.Close()
	// TODO: implement connection handling logic
}

func main() {
	var soc Server
	soc.host = "0.0.0.0"
	soc.port = 33728
	listener, err := net.Listen("tcp", ":"+fmt.Sprint(soc.port))
	if err != nil {
		fmt.Printf("Error starting server: %v\n", err)
		return
	}
	defer listener.Close()
	fmt.Printf("Server listening on %s:%d\n", soc.host, soc.port)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Printf("Error accepting connection: %v\n", err)
			continue
		}
		go handleConnection(conn)
	}
}
