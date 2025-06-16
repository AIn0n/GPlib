import re
import datetime
import os
import argparse


def org_to_post(
    input_file, title, author="Szymon Górka", layout="post", media_subpath=None
):
    tag_pattern = re.compile(r'<a id="org[a-f0-9]+"></a>\s*$')
    script_name = os.path.basename(__file__)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read lines from input file
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Filter lines
    filtered_lines = [line for line in lines if not tag_pattern.match(line.strip())]

    # Prepare output file path
    output_file = "cleaned_" + os.path.basename(input_file)
    output_file = os.path.join(os.path.dirname(input_file), output_file)

    # Prepare Jekyll front matter
    front_matter = (
        "---\n" f"title: {title}\n" f"author: {author}\n" f"layout: {layout}\n"
    )
    if media_subpath:
        front_matter += f"media_subpath: {media_subpath}\n"
    front_matter += "---\n\n"

    # Write to output file with front matter and comment
    with open(output_file, "w") as f:
        f.write(front_matter)
        f.write("<!--\n")
        f.write(f"modified at {date_str} by {script_name}\n")
        f.write("-->\n\n")
        f.writelines(filtered_lines)

    return output_file


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Convert org file to Jekyll post with front matter."
    )
    parser.add_argument("filename", type=str, help="Path to the input org file")
    parser.add_argument("title", type=str, help="Title for the post")
    parser.add_argument(
        "--author",
        type=str,
        default="Szymon Górka",
        help="Author name (default: Szymon Górka)",
    )
    parser.add_argument(
        "--media_subpath", type=str, default=None, help="Media subpath (optional)"
    )

    args = parser.parse_args()

    output = org_to_post(
        input_file=args.filename,
        title=args.title,
        author=args.author,
        media_subpath=args.media_subpath,
    )
    print(f"Output written to: {output}")
