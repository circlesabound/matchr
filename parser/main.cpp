#include <iostream>
#include <vector>
#include "include/json.hpp"

using json = nlohmann::json;

int main()
{
    std::vector<std::string> lines;
    for (std::string line; std::getline(std::cin, line); )
    {
        lines.push_back(line);
    }
    return 0;
}
