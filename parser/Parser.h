//
// Created by john on 10/1/16.
//

#ifndef PARSER_PARSER_H
#define PARSER_PARSER_H


#include <vector>
#include <string>
#include <map>

class Parser
{
public:
    struct brace_placement
    {
        using value = int;
        static constexpr brace_placement::value FAIL = -1;
        static constexpr brace_placement::value INLINE = 0;
        static constexpr brace_placement::value UNDERNEATH = 1;

        static brace_placement::value parse_line(const std::string& line);
    };

    struct space_or_tab
    {
        using value = int;
        static constexpr space_or_tab::value FAIL = -1;
        static constexpr space_or_tab::value SPACE = 0;
        static constexpr space_or_tab::value TAB = 1;

        static space_or_tab::value parse_line(const std::string& line);
    };

    struct indent_amount
    {
        using value = int;
        static constexpr indent_amount::value FAIL = -1;

        static indent_amount::value parse_line(const std::string& line);
    };

    struct var_convention
    {
        using value = int;
        static constexpr var_convention::value FAIL = -1;
        static constexpr var_convention::value CAMELCASE = 0;
        static constexpr var_convention::value SNAKECASE = 1;

        static var_convention::value parse_line(const std::string& line);
    };

    struct comment_style
    {
        using value = int;
        static constexpr comment_style::value FAIL = -1;
        static constexpr comment_style::value LINE = 0;
        static constexpr comment_style::value BLOCK = 1;

        static var_convention::value parse_line(const std::string& line);
    };

    struct max_line_length
    {
        using value = int;
        static constexpr max_line_length::value FAIL = -1;

        static max_line_length::value parse_line(const std::string& line);
    };

    Parser(const std::vector<std::string>& lines);

    brace_placement::value get_brace_placement();

    space_or_tab::value get_space_or_tab();

    indent_amount::value get_indent_amount();

    var_convention::value get_var_convention();

    comment_style::value get_comment_style();

    max_line_length::value get_max_line_length();

private:
    const std::vector<std::string>& lines;
    std::map<int, brace_placement::value> brace_placement_score;
    std::map<int, space_or_tab::value> space_or_tab_score;
    std::map<int, indent_amount::value> indent_amount_score;
    std::map<int, var_convention::value> var_convention_score;
    std::map<int, comment_style::value> comment_style_score;
    bool brace_placement;
    bool space_or_tab;
    bool indent_amount;
    bool var_convention;
    bool comment_style;
    max_line_length::value max_line_length_score;

    /**
     * Parse as many of the lines as possible, starting from the first line
     * @return the number of lines parsed
     */
    int parse();
};


#endif //PARSER_PARSER_H
