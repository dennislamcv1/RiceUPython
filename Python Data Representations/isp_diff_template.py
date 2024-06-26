"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    # Find the minimum length of the two lines
    min_len = min(len(line1), len(line2))
    
    # Compare characters of both lines up to the minimum length
    for index in range(min_len):
        if line1[index] != line2[index]:
            return index
    
    # If no differences found within the range of the shorter line,
    # check if the lengths of the lines are different
    if len(line1) != len(line2):
        return min_len
    
    # If lines are identical
    return IDENTICAL



def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    # Check for newline or carriage return characters
    if '\n' in line1 or '\r' in line1 or '\n' in line2 or '\r' in line2:
        return ""
    
    # Validate the index
    if not (0 <= idx <= min(len(line1), len(line2))):
        return ""
    
    # Construct the separator line
    separator_line = "=" * idx + "^"
    
    # Construct and return the formatted string with an extra newline at the end
    formatted_string = f"{line1}\n{separator_line}\n{line2}\n"
    return formatted_string




def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    # Find the minimum length of the two lists
    min_len = min(len(lines1), len(lines2))
    
    # Compare lines up to the length of the shorter list
    for line_index in range(min_len):
        char_index = singleline_diff(lines1[line_index], lines2[line_index])
        if char_index != IDENTICAL:
            return (line_index, char_index)
    
    # If no differences found within the range of the shorter list,
    # check if the lengths of the lists are different
    if len(lines1) != len(lines2):
        return (min_len, 0)
    
    # If lists are identical
    return (IDENTICAL, IDENTICAL)


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename. Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines



def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    lines1 = get_file_lines(filename1)
    lines2 = get_file_lines(filename2)
    
    line_index, char_index = multiline_diff(lines1, lines2)
    
    if line_index == IDENTICAL:
        return "No differences\n"
    
    diff_line1 = lines1[line_index]
    diff_line2 = lines2[line_index]
    formatted_diff = singleline_diff_format(diff_line1, diff_line2, char_index)
    
    return f"Line {line_index}:\n{formatted_diff}"
