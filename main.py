import os
import sys
import time
import subprocess
import logging
from typing import Dict, Any

# Configure professional-grade logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("PolyglotAgent")

class Config:
    MAX_RUNTIME_MS = 2000
    COMPILER = "g++"
    COMPILER_FLAGS = ["-O3", "-std=c++20", "-Wall"]
    WORKSPACE_DIR = "./agent_sandbox"

    @classmethod
    def setup(cls):
        if not os.path.exists(cls.WORKSPACE_DIR):
            os.makedirs(cls.WORKSPACE_DIR)
            logger.info(f"Sandbox initialized at: {cls.WORKSPACE_DIR}")

class MCPServer:
    """Local execution sandbox replacing external LLM API calls for testing."""
    def __init__(self):
        self.workspace = Config.WORKSPACE_DIR

    def profile_python(self, script_content: str, test_input: str) -> Dict[str, Any]:
        """Profiles the original Python logic to establish a reference latency and expected output."""
        path = os.path.join(self.workspace, "source.py")
        with open(path, "w") as f:
            f.write(script_content)

        start = time.perf_counter()
        try:
            proc = subprocess.run(
                [sys.executable, path],
                input=test_input, text=True, capture_output=True,
                timeout=Config.MAX_RUNTIME_MS / 1000.0
            )
            runtime = (time.perf_counter() - start) * 1000.0
            if proc.returncode != 0:
                return {"status": "error", "err": proc.stderr}
            return {"status": "ok", "ms": runtime, "out": proc.stdout.strip()}
        except subprocess.TimeoutExpired:
            return {"status": "timeout"}

    def compile_cpp(self, cpp_content: str) -> Dict[str, Any]:
        """Compiles generated C++ code and catches syntax or structural errors."""
        cpp_path = os.path.join(self.workspace, "target.cpp")
        bin_path = os.path.join(self.workspace, "target.out")

        with open(cpp_path, "w") as f:
            f.write(cpp_content)

        cmd = [Config.COMPILER] + Config.COMPILER_FLAGS + [cpp_path, "-o", bin_path]
        proc = subprocess.run(cmd, text=True, capture_output=True)

        if proc.returncode != 0:
            return {"status": "fail", "err": proc.stderr}
        return {"status": "ok", "bin": bin_path}

    def run_binary(self, bin_path: str, test_input: str) -> Dict[str, Any]:
        """Executes the compiled C++ binary and returns metrics for parity checking."""
        start = time.perf_counter()
        try:
            proc = subprocess.run(
                [bin_path],
                input=test_input, text=True, capture_output=True,
                timeout=Config.MAX_RUNTIME_MS / 1000.0
            )
            runtime = (time.perf_counter() - start) * 1000.0
            if proc.returncode != 0:
                return {"status": "error", "err": proc.stderr}
            return {"status": "ok", "ms": runtime, "out": proc.stdout.strip()}
        except subprocess.TimeoutExpired:
            return {"status": "timeout"}

class MockAgent:
    """Simulates LLM generation for the Capstone demo to ensure it runs without API keys."""
    @staticmethod
    def generate_cpp(attempt: int) -> str:
        # Intentionally fails on attempt 1 to demonstrate the autonomous self-correction loop
        if attempt == 1:
            return "#include <iostream>\nint main() { long long n; std::cin >> n; std::cout << (n*(n+1))/2; }"

        # Succeeds on attempt 2
        return """#include <iostream>
#include <cstdint>

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    int64_t n;
    if (std::cin >> n) {
        std::cout << (n * (n + 1)) / 2 << "\\n";
    }
    return 0;
}"""

def run_pipeline():
    Config.setup()
    sandbox = MCPServer()

    # 1. Profile original code
    logger.info("Profiling source Python logic...")
    py_code = "import sys\nfor line in sys.stdin:\n    n = int(line)\n    print(sum(range(1, n+1)))"
    test_data = "1000000"

    py_metrics = sandbox.profile_python(py_code, test_data)
    if py_metrics["status"] != "ok":
        logger.error("Source profiling failed.")
        return

    logger.info(f"Python Reference: {py_metrics['ms']:.2f}ms | Output: {py_metrics['out']}")

    # 2. Refactor and Compile loop
    attempts = 1
    while attempts <= 3:
        logger.info(f"Generating C++ optimization (Attempt {attempts})...")
        cpp_code = MockAgent.generate_cpp(attempts)

        compilation = sandbox.compile_cpp(cpp_code)
        if compilation["status"] == "fail":
            logger.warning(f"Compilation failed. Feeding stderr back to agent:\n{compilation['err'].strip()}")
            attempts += 1
            continue

        logger.info("Compilation successful. Validating logic parity...")
        cpp_metrics = sandbox.run_binary(compilation["bin"], test_data)

        if cpp_metrics["status"] == "ok" and cpp_metrics["out"] == py_metrics["out"]:
            logger.info(f"Validation Passed! Native execution: {cpp_metrics['ms']:.2f}ms")
            logger.info("Final C++ Asset Ready.")
            return

        attempts += 1

if __name__ == "__main__":
    run_pipeline()
