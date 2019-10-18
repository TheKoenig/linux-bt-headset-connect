# linux-bt-headset-connect

This tool should help keeping the connection to a Bluetooth headset alive.

It was developed and optimized for the use of
* Ubuntu 18.04 (running on a Lenovo T580)
* Bose SoundLink AE2

## <a name="use">How to use it</a>

### Calling the program directly

You can call the program via

    ./bt-headset-connect.py

If you want to have it available everywhere, run

    git clone https://github.com/SilverJan/linux-bt-headset-connect.git ~/dev/
    echo "PATH=$PATH:$HOME/dev/linux-bt-headset-connect/" >> ~/.bashrc

### Running the program as a daemon / on login

TBD

## Sources

The Bluetoothctl class mainly comes from https://gist.github.com/castis/0b7a162995d0b465ba9c84728e60ec01.