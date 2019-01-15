#include <stdio.h>
#include <string.h>
#include <signal.h>
#include "zmq.hpp"
#include "json.h"

static bool g_interrupted = false;

static void s_signal_handler (int signal_value)
{
    g_interrupted = true;
}

static void s_catch_signals ()
{
    struct sigaction action;
    action.sa_handler = s_signal_handler;
    //  Doesn't matter if SA_RESTART set because self-pipe will wake up zmq_poll
    //  But setting to 0 will allow zmq_read to be interrupted.
    action.sa_flags = 0;
    sigemptyset (&action.sa_mask);
    sigaction (SIGINT, &action, NULL);
    sigaction (SIGTERM, &action, NULL);

    signal(SIGHUP, SIG_IGN);
}

void onReceiveFREvent(json::JSON& jsonMsg) {
    std::string eventType = jsonMsg["type"].ToString();
    std::cout << "Event " << eventType << std::endl;
    if (eventType == "ADD") {
        std::cout << "Camera " << jsonMsg["camera"].ToString() << std::endl;
        json::JSON persons = jsonMsg["persons"];
        json::JSON personOne = persons[0];
        std::cout << "Person ID " << personOne["person"].ToInt() << std::endl;
    } else if (eventType == "OUT"){
        std::cout << "Camera " << jsonMsg["camera"].ToString() << std::endl;
    } else if (eventType == "CLEARED") {
        std::cout << "Camera " << jsonMsg["camera"].ToString() << std::endl;
    }
}

int main(int argc, char** argv)
{
    s_catch_signals();

    //  Prepare our context and socket
    zmq::context_t context (1);
    zmq::socket_t subscriber (context, ZMQ_SUB);
    // location of engine is localhost here. but it can also work over the network.
    // for example, "tcp://192.168.1.30:2687" would connect to the Camvi engine running
    // at 192.168.1.30
    const char* engineLocation = "tcp://localhost:2687";
    subscriber.connect(engineLocation);
    subscriber.setsockopt( ZMQ_SUBSCRIBE, "", 0);

    while (!g_interrupted) {
        std::cout << "Waiting to receive message...\n";

        zmq::message_t request;

        //  Wait for next request from client
        try
        {
            subscriber.recv( &request );
            if ( request.data() == NULL )
            {
                std::cout << "got null update request\n";
                continue;
            }
        }
        catch ( zmq::error_t err )
        {
            std::cout << "message subscriber exception: " << err.what() << std::endl;
            break;
        }

        std::string s( reinterpret_cast<char const*>(request.data()), request.size() ) ;
        std::cout << "received " << s << std::endl;

        json::JSON jsonMsg = json::JSON::Load(s);
        onReceiveFREvent(jsonMsg);
    }

    return 0;
}
