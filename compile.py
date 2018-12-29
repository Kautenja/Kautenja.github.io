"""Compile the HTML templates in this project into a complete project."""
import yaml


DEFAULTS = {
    'cv': '#',
    'tagline': 'Tagline',
    'avatar': 'http://placehold.it/700x300',
    'email': 'Email',
    'linkedin': 'https://linkedin.com',
    'name': 'Name',
    'github': 'Github',
}


def load_metadata(metadata_filename: str='metadata.yaml') -> dict:
    """
    Load the YAML metadata from disk and return it as a dictionary.

    Args:
        metadata_filename: the name of the YAML file to load

    Returns:
        a dictionary with the data from the YAML file

    """
    # read the YAML file and return it
    with open(metadata_filename, 'r') as metadata_file:
        return yaml.safe_load(metadata_file)


# a template for creating entries for an open source project
OPEN_SOURCE_PROJECTS_TEMPLATE = """
<!-- Project: {name} -->
<div class="row">
<div class="col-md-7">
{media}
</div>
<div class="col-md-5">
  <h3>{name}</h3>
  <p>{description}</p>
  <a class="btn btn-primary" href="{url}">View Project</a>
</div>
</div>
<!-- /.row -->
<hr>
""".lstrip()


# a template for images in the media section of open source templates
OPEN_SOURCE_IMG_TEMPLATE = """
  <a href="{url}">
    <img class="img-fluid rounded mb-3 mb-md-0" src="{img}" alt="{name}" />
  </a>
""".lstrip().rstrip()


# a template for videos in the media section of open source templates
OPEN_SOURCE_VID_TEMPLATE = """
  <center>
    <video class="img-fluid rounded mb-3 mb-md-0" controls>
      <source src="{vid}" type="video/mp4"/>
    </video>
  </center>
""".lstrip().rstrip()


def open_source_projects(metadata: dict) -> str:
    """
    Parse open source projects from a dictionary of metadata.

    Args:
        metadata: the dictionary containing the metadata

    Returns:
        a string of formatted HTML with the metadata information

    """
    rows = []
    for project in metadata.get('open_source_projects', []):
        # look for a video in the entry
        vid = project.get('vid', None)
        if vid is not None:
            # create the video from the format string
            media = OPEN_SOURCE_VID_TEMPLATE.replace('{vid}', vid)
        # if no video, look for an image
        else:
            # if no image, default to a placeholder image
            img = project.get('img', 'http://placehold.it/700x300')
            # create the image from the format string
            media = OPEN_SOURCE_IMG_TEMPLATE.replace('{img}', img)
        # place the media template into the project template
        html_project = OPEN_SOURCE_PROJECTS_TEMPLATE.replace('{media}', media)
        # unwrap the data with default values
        name = project.get('name', 'Name')
        desc = project.get('description', 'Description')
        url = project.get('url', '#')
        # update the project template with the data
        html_project = html_project.format(
            name=name,
            description=desc,
            url=url,
        )
        rows += [html_project]

    return '\n'.join(rows)


PUBLICATIONS_TEMPLATE = """
<!-- Project: {title} -->
<div class="row">
<div class="col-md">
  <h3>{title}</h3>
  <h4>{authors}</h4>
  <h5><b>{year}</b> <i>{venue}</i></h5>
  <p>{description}</p>
  <a class="btn btn-primary" href="{bib}">.bib</a>
  <a class="btn btn-primary" href="{pdf}">.pdf</a>
</div>
</div>
<!-- /.row -->
<hr>
""".lstrip()


def publications(metadata: dict) -> str:
    """
    Parse publications from the metadata.

    Args:
        metadata: the dictionary containing the metadata

    Returns:
        a string of formatted HTML with the metadata information

    """
    rows = []
    for project in metadata.get('publications', []):
        # unwrap the data with default values
        title = project.get('title', 'Title')
        authors = project.get('authors', 'Authors')
        year = project.get('year', 'Year')
        venue = project.get('venue', 'Venue')
        desc = project.get('description', 'Description')
        bib = project.get('bib', '#')
        pdf = project.get('pdf', '#')
        # create the HTML entry
        html_project = PUBLICATIONS_TEMPLATE.format(
            title=title,
            authors=authors,
            year=year,
            venue=venue,
            description=desc,
            bib=bib,
            pdf=pdf,
        )
        rows += [html_project]

    return '\n'.join(rows)


def write_file(basename: str, transform: 'Callable') -> None:
    """
    Open a template file, replace the sentinels, and write an output file.

    Args:
        basename: the name of the file (without extensions) to read and write
        transform:

    Returns:
        None

    """
    # open the template file
    with open('html/{}.html'.format(basename), 'r') as input_file:
        # read the file as a string
        html = input_file.read()
        # replace the body sentinel
        html = transform(html)
        # replace the metadata in the file
        html = html.replace('$$name$$', METADATA.get('name', DEFAULTS['name']))
        html = html.replace('$$github$$', METADATA.get('github', DEFAULTS['github']))
        html = html.replace('$$avatar$$', METADATA.get('avatar', DEFAULTS['avatar']))
        html = html.replace('$$email$$', METADATA.get('email', DEFAULTS['email']))
        html = html.replace('$$linkedin$$', METADATA.get('linkedin', DEFAULTS['linkedin']))
        html = html.replace('$$cv$$', METADATA.get('cv', DEFAULTS['cv']))
        html = html.replace('$$tagline$$', METADATA.get('tagline', DEFAULTS['tagline']))
        # write the output file
        with open('{}.html'.format(basename), 'w') as output_file:
            output_file.write(html)


if __name__ == '__main__':
    # load the metadata
    METADATA = load_metadata()
    # get the open source project HTML
    # write_file('index', 'open source projects', open_source_projects(METADATA))
    write_file('index', lambda x: x.replace('$$projects$$', open_source_projects(METADATA)))
    # write_file('publications', 'publications', publications(METADATA))
    write_file('publications', lambda x: x.replace('$$publications$$', publications(METADATA)))
    write_file('contact', lambda x: x)
