import random
import time
import statistics

# List of mock API relay endpoints with configurable names
RELAYS = [
    {"name": "relay-a.com", "base_latency": 0.1, "error_rate": 0.2},
    {"name": "relay-b.com", "base_latency": 0.3, "error_rate": 0.05},
    {"name": "relay-c.com", "base_latency": 0.2, "error_rate": 0.1},
]

def simulate_request(relay):
    """Simulate a request to a relay, returning success and latency."""
    time.sleep(relay["base_latency"] * 0.1)  # simulate small delay
    if random.random() < relay["error_rate"]:
        return False, relay["base_latency"] + random.uniform(0.2, 0.5)
    return True, relay["base_latency"] + random.uniform(0, 0.05)

def benchmark_relay(relay, trials=10):
    """Benchmark a relay: return success rate and average latency for successful calls."""
    latencies = []
    successes = 0
    for _ in range(trials):
        ok, latency = simulate_request(relay)
        if ok:
            successes += 1
            latencies.append(latency)
    success_rate = successes / trials
    avg_latency = statistics.mean(latencies) if latencies else float('inf')
    return success_rate, avg_latency

def select_best_relay(relays, min_success_rate=0.8):
    """Select the relay with best latency among those meeting success threshold."""
    candidates = []
    print("Benchmarking relays...")
    for relay in relays:
        success_rate, avg_latency = benchmark_relay(relay)
        print(f"  {relay['name']}: success={success_rate*100:.0f}% avg_latency={avg_latency*1000:.0f}ms")
        if success_rate >= min_success_rate:
            candidates.append((avg_latency, relay))
    if not candidates:
        print("No relay meets minimum success rate. Using default first.")
        return relays[0]
    candidates.sort()
    return candidates[0][1]

def main():
    best = select_best_relay(RELAYS)
    print(f"\nSwitching to best relay: {best['name']}")
    # Demo a request using the selected relay
    ok, latency = simulate_request(best)
    print(f"Test request to {best['name']}: {'success' if ok else 'failed'} ({latency*1000:.0f}ms)")

if __name__ == "__main__":
    main()
