Installation
============

To install DataVizQA, ensure you have put your API key a *.env* file - see the *.env.template* file for an example. 

Then run the following commands:

1. Clone the repository:
------------------------
.. code-block:: bash

   git clone https://github.com/your-username/data-viz-qa.git
   cd data-viz-qa        

2. Install dependencies using Poetry:
-------------------------------------
.. code-block:: bash

   poetry install      

3. Activate the virtual environment:
------------------------------------
.. code-block:: bash

   poetry shell      

4. Run the Streamlit application:
---------------------------------
.. code-block:: bash

   streamlit run src/data_viz/main.py      
