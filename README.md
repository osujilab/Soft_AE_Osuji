<b> <h1> Autonomous Experimentation (AE) Codebase for the Soft-AE Setup, Osuji Lab </h1> </b>
<h4> Department of Chemical and Biomolecular Engineering, University of Pennsylvania </h4>
<h4> Created: November 2024 </h4>

For information, please contact one of the Soft AE Admins or the Osuji lab PI: cosuji@seas.upenn.edu

<b>PI:</b> Chinedum Osuji 

**Admins:** Chris Johnson, Pavel Shapturenka, Yvonne Zagzag

**Additional Users:** Justin Hughes, Po-ting Lin

Current Soft-AE functionality integrates stage motion, liquid dispensing, and polarized optical microscopy to afford high-throughput soft material formulation and inspection. These capabilities also enable bulk electrical and ionic conductivity measurements via four-point resistivity and basic impedance spectroscopy analysis, respectively, which are under active development. High-throughput methods are extended to autonomous experimentation *via* in-loop implementation of algorithms such as Bayesian optimization and Gaussian process-informed parameter phase space exploration.

All capabilities are currently being packaged into a graphical user interface via tkinter, featuring manual instrument control and human-in-the-loop (HITL) experimentation. 

All Soft-AE functionality is organized into classes (located in ./SoftAE_classPkg). Each instrument capability is imported from this directory and initialized as a class instance, with default values specified for the specific setup in the Osuji lab in the class definition.

High-throuhgput and AE campaigns are currently run via Jupyter notebooks by importing all required dependencies and running initialization codeblocks that handle liquid dispensing and ensure instrument connectivity.

<div style="width: 1160px; height: 624px;">
    <img src="https://github.com/user-attachments/assets/9c3b68e6-0f35-4500-9d69-05e6089ae3ed" width="62%" height="62%">
    <img src="https://github.com/user-attachments/assets/a399800e-c51a-4440-82a7-eb72cccfdd47" width="25%" height="25%">
</div>

