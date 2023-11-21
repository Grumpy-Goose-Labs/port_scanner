import asyncio
import time

class Scanner:
    def __init__(self, target_host, target_ports):
        self.target_host = target_host
        self.target_ports = target_ports

    async def scan_port(self, target_port):
        try:
            reader, writer = await asyncio.open_connection(self.target_host, target_port)
            print(f'[+] Connection established on {self.target_host}:{target_port}')
            writer.close()
        except (asyncio.TimeoutError, OSError):
            # only for verbosity or debugging...
            # print(f'[-] Connection failed on {self.target_host}:{target_port}')
            pass
    
    async def port_scan(self):
        try:
            target_ip = await asyncio.get_running_loop().getaddrinfo(self.target_host, None)
            target_ip = target_ip[0][4][0]

        except OSError as e:
            print(f'[-] Cannot resolve {self.target_host}: {e}')
            return
        
        start_time = time.time()

        scan_tasks = [self.scan_port(port) for port in self.target_ports]
        await asyncio.gather(*scan_tasks)

        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f'\n[+] Scan finished in {round(elapsed_time, 2)} seconds.')

if __name__ == '__main__':
    target_host = input("Enter the host to be scanned: ")
    target_ports = range(1, 65535)

    scanner = Scanner(target_host, target_ports)
    asyncio.run(scanner.port_scan())