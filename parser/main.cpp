#include <iostream>
#include <vector>
#include "include/json.hpp"
#include "Parser.h"

using json = nlohmann::json;

int main()
{
    std::vector<std::string> lines;
    for (std::string line; std::getline(std::cin, line); ) lines.push_back(line);
    Parser parser(lines);
    json output;
    output["bracePlacement"] = parser.get_brace_placement();
    output["spaceOrTab"] = parser.get_space_or_tab();
    output["indentAmount"] = parser.get_indent_amount();
    output["varConvention"] = parser.get_var_convention();
    output["commentStyle"] = parser.get_comment_style();
    output["maxLineLength"] = parser.get_max_line_length();
    std::cout << output.dump(4) << std::endl;
    return 0;
}
