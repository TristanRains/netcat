# netcat
A python script that imitates basic netcat functionality and allows basic command execution

## Arguments

* `--listen` - listens for incoming connections, requires a port number 
* `--connect` - makes a socket connection, requires an address followed by a port number

## Example usage:

```bash
python3 --listen 8080
python3 --connect 127.0.0.1 8080
```

## Test case:

**server-side**

```bash
python3 --listen 80
```
**client-side**

```bash
python3 --connect 127.0.0.1 80
whoami
ls -l
pwd
```
