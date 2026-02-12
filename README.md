# Dropception Quant - Double Emulsion Quantification Tool

This application is a Python-based GUI for analyzing double emulsions (DEs) from multi-channel microscope images (OME-TIFF). It features automatic segmentation, background correction, and statistical analysis tailored for high-throughput microfluidic data.

## Prerequisites

* **Python 3.8** or higher installed on your system.
* (Optional but Recommended) **Anaconda** or **Miniconda** for environment management.

---

## Installation & Setup

It is highly recommended to run this application in a virtual environment to avoid conflicts with other Python projects.

### Option A: Using venv (Standard Python)

1.  **Open your terminal/command prompt** and navigate to the folder containing the script and `requirements.txt`.
2.  **Create a virtual environment**:
    * Windows: `python -m venv venv`
    * Mac/Linux: `python3 -m venv venv`
3.  **Activate the environment**:
    * Windows: `.\venv\Scripts\activate`
    * Mac/Linux: `source venv/bin/activate`
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Option B: Using Conda (Anaconda/Miniconda)

1.  **Open your terminal/Anaconda Prompt**.
2.  **Create a new environment**:
    ```bash
    conda create --name de_analyzer python=3.9
    ```
3.  **Activate the environment**:
    ```bash
    conda activate de_analyzer
    ```
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Application

1.  Ensure your environment is activated (you should see `(venv)` or `(de_analyzer)` in your terminal prompt).
2.  Run the Python script:
    ```bash
    python dropception-quant.py
    ```

---

## Interface Features & Guide

**A.  View Layers (Image Compositing)**

Located in the "View Layers" panel, this gives you control over how you visualize your multi-channel data.

*   **Visibility Checkbox:** Toggle individual channels on or off. You can view Brightfield and Fluorescence channels simultaneously (overlaid).

*   **Color Dropdown:** Assign pseudo-colors (Green, Red, Cyan, Magenta, Yellow, etc.) to each channel to match your fluorophores.

*   **Clip Slider (0-255):** This acts as a "Black Level" or background threshold.

    *   **Slide Right:** Increases the threshold, cutting out dim background pixels.

    * **Usage:** Essential for fluorescence channels. Increase this slider until the hazy background disappears and only the bright droplets remain visible on top of the Brightfield image.

**B.  Segmentation (Finding Droplets)**

Controls the Hough Circle Transform algorithm used to identify the distinct dark rings of double emulsions.

*   **Show Cyan Overlay:** Uncheck this to temporarily hide the segmentation circles, allowing you to compare the detection accuracy against the raw image.

*   **Edge (Param 1):** The Canny edge detection threshold.

    *   Increase if the tool is detecting too much noise/texture as edges.

    *   Decrease if it fails to see the outline of the droplets.

*   **Circ (Param 2):** The accumulator threshold.

    *   Lower values detect more faint circles (risk of false positives).

    *   Higher values detect only the most perfect circles.

*   **MinR / MaxR:** The expected minimum and maximum radius (in pixels) of your droplets.

**C.    Analysis Settings**

*   **Set Analysis ROI (Crop):** This setting allows you to select which portion of the image to analyze. The image can often have a "vignette" that impacts the background signal you subtract against and can also negatively impact measurements of DEs inside darker areas, so setting the ROI can help minimize measurement artifacts.

*   **Shrink ROI (px):** This setting peels layers of pixels off the outer edge of the detected circle before measuring intensity.

    *   **Why use it?** Double emulsions have thick dark rings. You want to measure the fluorescence of the inner core, avoiding the dark ring or the oil shell. Increasing this value samples more from the bright core and can reduce artifacts in quantification that increase variability.

*   **Background Mode:**

    *   **Auto BG:** Automatically calculates background by taking the average intensity of "empty space" (pixels not inside any detected droplet).

    *   **Manual BG:** Allows you to draw a rectangle on the image to explicitly define the background region.

*   **Graph Channel:** A dropdown to select which channel is currently displayed on the plot (e.g., "Channel 2"). Changing this instantly updates the histogram and statistics without needing to re-calculate.

**D.    Stats & Plots**

*   **Histogram:** Displays the distribution of intensities (background-subtracted) for the selected channel.

*   **KDE (Red Line):** A Kernel Density Estimation curve that smooths the histogram to visualize the population shape.

*   **Stats Panel:**

    *   **Mean/Std:** Standard arithmetic mean and standard deviation.

    *   **KDE Peak:** The "Mode" of the distribution. This is often more accurate than the Mean for skewed populations (e.g., if a few bright outliers pull the average up).

*   **Save Plot Image:** Exports the currently visible graph as a .png file for presentations.

## Suggested Workflow

1. **Load Image:** Click "Load OME-TIFF" to open your multi-channel image stack.

2.  **Setup Visualization:**

    *   Set your Brightfield channel (usually Ch1) to Gray.

    *   Set your Fluorescence channel (e.g., Ch2) to Green.

    *   Increase the Clip Slider for the Green channel until the background haze disappears, leaving only the droplets glowing.

3.  **Tune Segmentation:**

    *   Adjust MinR and MaxR until the cyan circles roughly match your droplet sizes.

    *   Use Right-Click + Drag to pan and Scroll to zoom in for a closer look.

4.  **Validate Selection:**

    *   Left-Click on any cyan circle that is an error (e.g., dirt, oil drop). It will turn Red and be excluded from calculations.

5.  **Analyze & Export:**

    *   Set the analysis ROI (crop) to your desired area.

    *   Set Shrink ROI to a pixel value that isolates the droplet cores and minimizes variability.

    *   Use the Graph Channel dropdown to check the data quality for each fluorophore.

    *   Click Export CSV to save a spreadsheet containing row-by-row data (ID, Radius, Raw Intensity, Net Intensity) for every droplet.

## Understanding the Exported Excel File

The tool exports a `.xlsx` file containing row-by-row data for every detected double emulsion and the parameters and distribution information for each channel.

### Summary Page

**Parameters:**

*   **Edge Thresh:** See Segmentation
*   **Circ Thresh:** See Segmentation
*   **Min/Max Radius:** See Segmentation
*   **Shrink ROI:** See Analysis Settings
*   **Background Mode:** See Analysis Settings
*   **Analysis region:** Region selected for analysis (modified if crop is used).
*   **Total Area:** Area analyzed in px^2. Can be used to calculate concentration if you can convert pixels to absolute area measurements.

**Summary Stats:**

*   **Channel:** The channel selected for the measurement.
*   **N (Count):** Number of DEs in selection.
*   **Area (px^2):** Area of selection for analysis.
*   **Density (N/px^2:**) Can be equated to DE concentration if you can convert pixels to absolute area measuements and know the height of the slide.
*   **Mean:** Mean intensity of DEs in the channel (subtracting background).
*   **Std Dev:** Standard deviation of intensity measurements for DEs in the channel.
*   **KDE Peak:** The mode of the smoothed distribution of DE intensities in the channel.
*   **Background Used:** Calculated intensity for the background of the selection space by which other intensities are subtracted against.


### Droplet Data Page

**General Info:**

* **`ID`**: The unique identifier for each droplet (corresponds to the ID shown in the hover tooltip).
* **`Valid`**: A `True` / `False` flag.
    * `True`: The droplet was included in the analysis.
    * `False`: The droplet was manually excluded (turned red) by the user.

**Geometric Measurements:**

* **`R_BF` (Radius Brightfield)**: The radius (in pixels) of the droplet as detected by the segmentation algorithm on the Brightfield channel (the cyan circle).
* **`R_Fluor` (Radius Fluorescence)**: The "shrunk" radius used for intensity measurement.
    * *Calculation:* `R_BF` minus the "Shrink ROI" value.
    * *Purpose:* Ensures measurement of the **inner core** only.

**Intensity Measurements:**

For each channel (Ch1, Ch2, etc.), there are two columns:

* **`ChX_Raw` (Raw Intensity)**: The mean pixel intensity inside the `R_Fluor` circle. This is the direct measurement from the image without any modification.
* **`ChX_Net` (Net Intensity)**: The background-corrected intensity.
    * *Calculation:* `ChX_Raw` minus the calculated Background value for that channel.
    * *Usage:* Use this value for scientific analysis (plotting, comparing concentrations), as it removes the baseline noise.