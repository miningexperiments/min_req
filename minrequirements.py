import psutil
import shutil
import sys
import platform
import multiprocessing
import time

try:
    import speedtest
except ModuleNotFoundError:
    print("❌ Missing dependency: 'speedtest-cli'")
    print("🔧 Install it using: pip install speedtest-cli")
    sys.exit(1)

MIN_CORES = 4
MIN_RAM_GB = 16
MIN_DISK_GB = 300
MIN_DL_SPEED = 40
MIN_UL_SPEED = 10
MIN_PING = 250


def bytes_to_mbps(bytes_per_second):
    return round(bytes_per_second / 1_000_000, 2)


def check_system_requirements():
    # Check CPU cores
    cpu_cores = multiprocessing.cpu_count()
    if cpu_cores < MIN_CORES:
        raise RuntimeError(
            f"Insufficient CPU cores: {cpu_cores} detected, {MIN_CORES} required."
        )

    # Check RAM
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes / (1024**3)
    if ram_gb < MIN_RAM_GB:
        raise RuntimeError(
            f"Insufficient RAM: {ram_gb:.2f} GB detected, {MIN_RAM_GB} GB required."
        )

    # Check available disk space
    disk_usage = shutil.disk_usage("/")
    disk_free_gb = disk_usage.free / (1024**3)
    if disk_free_gb < MIN_DISK_GB:
        raise RuntimeError(
            f"Insufficient disk space: {disk_free_gb:.2f} GB free, {MIN_DISK_GB} GB required."
        )

    print("✅ System resource check passed.")
    print(
        f"  Cores: {cpu_cores}, RAM: {ram_gb:.2f} GB, Free disk: {disk_free_gb:.2f} GB"
    )


def run_speed_test():
    print("\nInitializing speed test...")
    st = speedtest.Speedtest()
    st.get_best_server()
    server = st.results.server
    print(f"Using server: {server['sponsor']} ({server['name']}, {server['country']})")

    print("Testing download speed...")
    download_speed = st.download()
    if download_speed < MIN_DL_SPEED:
        raise RuntimeError(
            f"Slow download speed: {download_speed} Mbps, {MIN_DL_SPEED} Mbps recommended."
        )

    print("Testing upload speed...")
    upload_speed = st.upload()
    if upload_speed < MIN_UL_SPEED:
        raise RuntimeError(
            f"Slow upload speed: {upload_speed} Mbps, {MIN_UL_SPEED} Mbps recommended."
        )

    print("Testing ping...")
    ping = st.results.ping
    if ping > MIN_PING:
        raise RuntimeError(
            f"High latency detected: {ping:.2f} ms, less than {MIN_PING} ms recommended."
        )

    print("✅ Internet checks passed.\n")
    print("\n=== Internet Speed Test Results ===")
    print(f"Ping (latency): {ping:.2f} ms")
    print(f"Download speed: {bytes_to_mbps(download_speed)} Mbps")
    print(f"Upload speed:   {bytes_to_mbps(upload_speed)} Mbps")
    print("===================================")


def main():
    t0 = time.time()

    print(f"Platform: {platform.system()} {platform.release()}\n")
    try:
        check_system_requirements()
        run_speed_test()
    except Exception as e:
        print(f"❌ Error: {e}")
    print(f"\nCompleted in {round(time.time() - t0, 2)} seconds.")


if __name__ == "__main__":
    main()
