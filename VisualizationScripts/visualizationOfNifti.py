import os
import SimpleITK as sitk
import vtk
from vtk.util import numpy_support
import math


def load_nifti_file(file_path):
    image = sitk.ReadImage(file_path)
    return image

def visualize_and_save_image(image, output_folder, person_id):
    # Convert the SimpleITK image to a VTK image
    img_array = sitk.GetArrayFromImage(image)
    vtk_data_array = numpy_support.numpy_to_vtk(num_array=img_array.ravel(), deep=True, array_type=vtk.VTK_FLOAT)

    # Create a VTK image
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(img_array.shape[2], img_array.shape[1], img_array.shape[0])
    vtk_image.SetSpacing(image.GetSpacing()[0], image.GetSpacing()[1], image.GetSpacing()[2])
    vtk_image.GetPointData().SetScalars(vtk_data_array)

    # Setup the visualization pipeline
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputData(vtk_image)

    volume_property = vtk.vtkVolumeProperty()
    volume_property.ShadeOn()
    volume_property.SetInterpolationTypeToLinear()

    # Create transfer functions for opacity and color
    opacity_transfer_function = vtk.vtkPiecewiseFunction()
    opacity_transfer_function.AddPoint(-3024, 0.0)  # Air
    opacity_transfer_function.AddPoint(-1000, 0.0)  # Lung
    opacity_transfer_function.AddPoint(-500, 0.0)  # Fat
    opacity_transfer_function.AddPoint(0, 0.2)  # Soft tissue
    opacity_transfer_function.AddPoint(300, 0.4)  # Muscle
    opacity_transfer_function.AddPoint(500, 0.6)  # Bone start
    opacity_transfer_function.AddPoint(1000, 0.8)  # Dense bone
    opacity_transfer_function.AddPoint(3071, 1.0)  # Maximum

    color_transfer_function = vtk.vtkColorTransferFunction()
    color_transfer_function.AddRGBPoint(-3024, 0.0, 0.0, 0.0)  # Air
    color_transfer_function.AddRGBPoint(-1000, 0.5, 0.5, 0.5)  # Lung
    color_transfer_function.AddRGBPoint(-500, 0.8, 0.6, 0.4)  # Fat
    color_transfer_function.AddRGBPoint(0, 0.9, 0.7, 0.6)  # Soft tissue
    color_transfer_function.AddRGBPoint(300, 0.95, 0.8, 0.7)  # Muscle
    color_transfer_function.AddRGBPoint(500, 1.0, 0.8, 0.8)  # Bone
    color_transfer_function.AddRGBPoint(1000, 0.9, 0.9, 1.0)  # Dense bone
    color_transfer_function.AddRGBPoint(3071, 1.0, 1.0, 1.0)  # Maximum

    volume_property.SetScalarOpacity(opacity_transfer_function)
    volume_property.SetColor(color_transfer_function)

    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    # Setup the rendering components
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    renderer.AddVolume(volume)
    renderer.SetBackground(0, 0, 0)
    render_window.SetSize(800, 800)

    # Set up the camera
    camera = renderer.GetActiveCamera()

    # Define camera angles for different views (0, 5, 10, 15, 20 degrees around the Y-axis)
    ORIENTATIONCONSTANT = 180
    angles = [ORIENTATIONCONSTANT + 0]
    distance = 1100  # Distance from the focal point (slightly zoomed in)

    view_up_vector = (0, 0, 1)  # Consistent view-up vector

    for idx, angle in enumerate(angles):
        radian_angle = math.radians(angle)
        position = (distance * math.sin(radian_angle), -distance * math.cos(radian_angle), 0)

        camera.SetPosition(position)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(view_up_vector)

        # Ensure the camera is set to see the volume
        renderer.ResetCamera()
        camera.Dolly(1.4)  # Slight zoom
        renderer.ResetCameraClippingRange()

        # Render and save screenshot
        render_window.Render()
        window_to_image_filter = vtk.vtkWindowToImageFilter()
        window_to_image_filter.SetInput(render_window)
        window_to_image_filter.Update()

        writer = vtk.vtkPNGWriter()
        output_path = os.path.join(output_folder, f'person_{person_id}_view_{idx}.png')
        writer.SetFileName(output_path)
        writer.SetInputConnection(window_to_image_filter.GetOutputPort())
        writer.Write()


def process_all_folders(base_directory, SUBFOLDERDIRECTORY, OUTPUTDIRNAME, STARTINDEX, ENDINDEX):
    output_folder = os.path.join(base_directory, OUTPUTDIRNAME)
    os.makedirs(output_folder, exist_ok=True)
    

    for i in range(STARTINDEX, ENDINDEX):  # Adjust range to include 0 to 300
        directory = base_directory + f'/{SUBFOLDERDIRECTORY}/{i}'
        print(directory)
        if os.path.isdir(directory):
            nifti_files = [f for f in os.listdir(directory) if f.endswith('.nii') or f.endswith('.nii.gz')]
            if not nifti_files:
                print(f"No NIfTI files found in directory: {directory}")
                continue
            
            for nifti_file in nifti_files:
                file_path = os.path.join(directory, nifti_file)
                try:
                    print(f"Processing file: {file_path}")
                    image = load_nifti_file(file_path)
                    visualize_and_save_image(image, output_folder, i)
                except Exception as e:
                    print(f"Failed to process file {file_path}: {e}")

if __name__ == "__main__":
    BASEDIR = r'/Users/avnoorludhar/Desktop/uwindsor/Glendor/visualizingNiftyFiles'  # Replace with the path to your base directory
    SUBFOLDERDIRECTORY = 'pyDefaceCleaned' #replace with subfolder that has the niftis
    OUTPUTDIRNAME = 'pictures'
    STARTINDEX = 0
    ENDINDEX = 300
    process_all_folders(BASEDIR, SUBFOLDERDIRECTORY, OUTPUTDIRNAME, STARTINDEX, ENDINDEX)
