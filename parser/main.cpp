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
    output["brace_placement"] = parser.get_brace_placement();
    output["space_or_tab"] = parser.get_space_or_tab();
    output["indent_amount"] = parser.get_indent_amount();
    output["var_convention"] = parser.get_var_convention();
    output["comment_style"] = parser.get_comment_style();
    output["max_line_length"] = parser.get_max_line_length();
    std::cout << output.dump(4) << std::endl;
    return 0;
}
