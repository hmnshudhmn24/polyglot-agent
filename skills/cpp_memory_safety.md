# Agent Skill: Modern C++20 Memory & Syntax Standards

When generating C++ code, you must adhere to modern C++20 standards. The target environment is a strict, performance-critical pipeline.

## Implementation Standards:
1.  **Fast I/O is mandatory:** Every `main()` function handling standard input must begin with:
    `std::ios_base::sync_with_stdio(false);`
    `std::cin.tie(NULL);`
2.  **No raw pointers:** Do not use `new` or `delete`. Use `std::unique_ptr` or `std::shared_ptr` if dynamic allocation is strictly required. Prefer stack allocation (`std::vector`) wherever possible.
3.  **Use fixed-width integers:** Use `<cstdint>`. Prefer `int64_t` over `long long` when dealing with large algorithmic constraints to prevent silent overflow errors.
4.  **Pass by const reference:** Always pass large containers (like `std::vector` or `std::string`) to functions using `const &` to avoid expensive copies.
5.  **Return 0:** The program must exit cleanly with `return 0;` to signal to the MCP server that execution succeeded.