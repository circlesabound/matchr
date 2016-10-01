//
// Created by john on 10/1/16.
//

#include <regex>
#include <iostream>

#include "Parser.h"

Parser::Parser(const std::vector<std::string>& lines)
        : lines{lines}
{
    this->brace_placement = false;
    this->space_or_tab = false;
    this->indent_amount = false;
    this->var_convention = false;
    this->comment_style = false;
    this->parse();
}

int Parser::parse()
{
    int i;
    for (i = 0; i < this->lines.size(); ++i)
    {
        const std::string& current_line = this->lines[i];

        // easy stuff
        int res;
        if ((res = brace_placement::parse_line(current_line)) != brace_placement::FAIL)
        {
            ++this->brace_placement_score[res];
            this->brace_placement = true;
        }
        if ((res = space_or_tab::parse_line(current_line)) != space_or_tab::FAIL)
        {
            ++this->space_or_tab_score[res];
            this->space_or_tab = true;
        }
        if ((res = var_convention::parse_line(current_line)) != var_convention::FAIL)
        {
            ++this->var_convention_score[res];
            this->var_convention = true;
        }
        if ((res = comment_style::parse_line(current_line)) != comment_style::FAIL)
        {
            ++this->comment_style_score[res];
            this->comment_style = true;
        }
        if ((res = indent_amount::parse_line(current_line)) != indent_amount::FAIL && res != 0)
        {
            ++this->indent_amount_score[res];
            this->indent_amount = true;
        }

        // a bit more complicated
        max_line_length::value result = max_line_length::parse_line(current_line);
        if (result > this->max_line_length_score) this->max_line_length_score = result;
    }

    return i;
}

Parser::brace_placement::value Parser::brace_placement::parse_line(const std::string& line)
{
    static const std::regex brace_at_end_regex("\\{[ \t]*$");
    static const std::regex brace_at_start_regex("^[ \t]*\\{[ \t]*$");
    if (std::regex_search(line, brace_at_start_regex)) return brace_placement::UNDERNEATH;
    if (std::regex_search(line, brace_at_end_regex)) return brace_placement::INLINE;
    return brace_placement::FAIL;
}

Parser::space_or_tab::value Parser::space_or_tab::parse_line(const std::string& line)
{
    static const std::regex tab_regex("^\t");
    static const std::regex space_regex("^ ");
    if (std::regex_search(line, tab_regex)) return space_or_tab::TAB;
    if (std::regex_search(line, space_regex)) return space_or_tab::SPACE;
    return space_or_tab::FAIL;
}

Parser::indent_amount::value Parser::indent_amount::parse_line(const std::string& line)
{
    static const std::regex leading_spaces("^( *)[^ \t].*$");
    static indent_amount::value previous = 0;
    std::smatch spaces_match;
    if (std::regex_search(line, spaces_match, leading_spaces))
    {
        indent_amount::value result = (indent_amount::value) spaces_match[1].length();
        indent_amount::value difference = (indent_amount::value) std::abs(previous - result);
        previous = result;
        return difference;
    }
    return indent_amount::FAIL;
}

Parser::var_convention::value Parser::var_convention::parse_line(const std::string& line)
{
    static const std::regex camel_regex("(^|[^A-Za-z0-9_.])([A-Za-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*) ?=");
    static const std::regex snake_regex("(^|[^A-Za-z0-9_.])([A-Za-z_][A-Za-z0-9]*_[A-Za-z0-9]*) ?=");
    if (std::regex_search(line, camel_regex)) return var_convention::CAMELCASE;
    if (std::regex_search(line, snake_regex)) return var_convention::SNAKECASE;
    return var_convention::FAIL;
}

Parser::var_convention::value Parser::comment_style::parse_line(const std::string& line)
{
    static const std::regex block_comment_regex("(/\\*)|(\\*/)");
    static const std::regex line_comment_regex("//");
    if (std::regex_search(line, line_comment_regex)) return comment_style::LINE;
    if (std::regex_search(line, block_comment_regex)) return comment_style::BLOCK;
    return comment_style::FAIL;
}

Parser::max_line_length::value Parser::max_line_length::parse_line(const std::string& line)
{
    return (max_line_length::value) line.size();
}

bool element_cmp(const std::pair<const int, int>& lhs, const std::pair<const int, int>& rhs)
{
    return lhs.second < rhs.second;
}

Parser::brace_placement::value Parser::get_brace_placement()
{
    int count = this->brace_placement_score[int(brace_placement::INLINE)] +
                this->brace_placement_score[int(brace_placement::UNDERNEATH)];
    int sum = this->brace_placement_score[int(brace_placement::INLINE)] * int(brace_placement::INLINE) +
              this->brace_placement_score[int(brace_placement::UNDERNEATH)] * int(brace_placement::UNDERNEATH);
    if (count <= brace_placement::MIN_SAMPLE_SIZE) return sum;
    else return sum * 20 / count;
}

Parser::space_or_tab::value Parser::get_space_or_tab()
{
    int count = this->space_or_tab_score[int(space_or_tab::SPACE)] +
                this->space_or_tab_score[int(space_or_tab::TAB)];
    int sum = this->space_or_tab_score[int(space_or_tab::SPACE)] * int(space_or_tab::SPACE) +
              this->space_or_tab_score[int(space_or_tab::TAB)] * int(space_or_tab::TAB);
    if (count <= space_or_tab::MIN_SAMPLE_SIZE) return sum;
    else return sum * 20 / count;
}

Parser::indent_amount::value Parser::get_indent_amount()
{
    if (!this->indent_amount) return indent_amount::FAIL;
    return std::max_element(
            this->indent_amount_score.cbegin(),
            this->indent_amount_score.cend(),
            &element_cmp
    )->first;
}

Parser::var_convention::value Parser::get_var_convention()
{
    int count = this->var_convention_score[int(var_convention::CAMELCASE)] +
                this->var_convention_score[int(var_convention::SNAKECASE)];
    int sum = this->var_convention_score[int(var_convention::CAMELCASE)] * int(var_convention::CAMELCASE) +
              this->var_convention_score[int(var_convention::SNAKECASE)] * int(var_convention::SNAKECASE);
    if (count <= var_convention::MIN_SAMPLE_SIZE) return sum;
    else return sum * 20 / count;
}

Parser::comment_style::value Parser::get_comment_style()
{
    int count = this->comment_style_score[int(comment_style::BLOCK)] +
                this->comment_style_score[int(comment_style::LINE)];
    int sum = this->comment_style_score[int(comment_style::BLOCK)] * int(comment_style::BLOCK) +
              this->comment_style_score[int(comment_style::LINE)] * int(comment_style::LINE);
    if (count <= comment_style::MIN_SAMPLE_SIZE) return sum;
    else return sum * 20 / count;
}

Parser::max_line_length::value Parser::get_max_line_length()
{
    return this->max_line_length_score;
}
