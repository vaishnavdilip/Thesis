import plotly.graph_objects as go
import plotly.express as px

plot_dirs = {
    "HTML_PLOT_DIR" : 'C:/Users/nikte/OneDrive - KU Leuven/Thesis_code/plots/html/',
    "PNG_PLOT_DIR" : 'C:/Users/nikte/OneDrive - KU Leuven/Thesis_code/plots/png/',
    "SVG_PLOT_DIR" : 'C:/Users/nikte/OneDrive - KU Leuven/Thesis_code/plots/svg/'
}


def export_plot(file, filename, format):
    """Function to export plot to different formats.

    Args:
        file (_type_): _description_
        filename (_type_): _description_
        format (_type_): _description_
    """

    for form in format:
        if form in ["png", "jpg", "jpeg","webp","eps","pdf","svg"]:
            location = plot_dirs[form.upper()+"_PLOT_DIR"]
            file.write_image(location + filename+'.'+form)
        elif form in ['html']:
            location = plot_dirs[form.upper()+"_PLOT_DIR"]
            file.write_html(location + filename+'.'+form)
    
    return 'Exported'