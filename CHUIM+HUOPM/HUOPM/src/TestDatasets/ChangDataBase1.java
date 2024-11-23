package TestDatasets;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;

public class ChangDataBase1 {
	static int tidCount = 0; 
	    
	public static void main(String[] args) {


 		int negativeItems = 0;
 		int sizeOfItems = 1657;
 		double ratioOfNegativeItems = 0.05;
 		
	     try {
	    	// ×xÈ¡¶à‚€ÙYÁÏŽì
	 		///////////////////////////////////////////////////////////////////////////////
 
	    	//**************  Note that  ************** 
	    	// foodmart has its own real unit profit values 
	    	// T10I4D100K  T40I10D100K   retail  BMSPOS2 kosarak (salePriceOfProduct <= 10)  
	    	// pumsb (salePriceOfProduct <= 100)
	    	// mushroom chess (salePriceOfProduct <= 30)  
	    	//**************  Note that  **************
	    	 
	    	final String[] filename1 = { "src/TestDatasets/BMSPOS2_UM_UtilityTable.txt"};  
	 		final String[] filename2 = { "src/TestDatasets/BMSPOS2_UM_NegativeUTable.txt"};  //DiscountTable
	 		///////////////////////////////////////////////////////////////////////////////

	 		
            // built the discount-table
	 		/******************************************************
	 		 ************  Item: strategy, v1, v2  ****************
	 		 ******************************************************/
	 		for(int i=0; i < 1; i++){
//		    	 FileReader file = new FileReader("C:/data_change/transaction.txt");
//		         File fileWrite = new File("C:/data_change/1.txt");
		    	 FileReader file = new FileReader(filename1[i]);
		         File fileWrite = new File(filename2[i]);
		    	 BufferedReader bufferedreader = new BufferedReader(file);
		         BufferedWriter writer = new BufferedWriter(new FileWriter(fileWrite));
		         String thisLine;              

		         while ((thisLine = bufferedreader.readLine()) != null) {
			         String str = "";
			         
					// split the transaction according to the : separator
					String[] data = thisLine.split(", ");
					double salePriceOfProduct = Double.valueOf(data[1]);
					// strategy 1.1: 100% 
					if(salePriceOfProduct <= 10 
							&& negativeItems < sizeOfItems*ratioOfNegativeItems){
						// strategy 1.1: 100% 
						str = data[0] + ", " + String.valueOf(0-Double.valueOf(data[1]));
						negativeItems++;
						
//					}else if(salePriceOfProduct > 20 && salePriceOfProduct <= 50
//							 && negativeItems < sizeOfItems*ratioOfNegativeItems){
//						// strategy 1.2: 0% 
//						str = data[0] + ", " + String.valueOf(0-Double.valueOf(data[1]));
//						negativeItems++;
//						
//					}else if(salePriceOfProduct > 50 && salePriceOfProduct <= 70
//							 && negativeItems < sizeOfItems*ratioOfNegativeItems){
//						// strategy 1.3: [10%, 90%] 
//						str = data[0] + ", " + String.valueOf(0-Double.valueOf(data[1]));
//						negativeItems++;
						
					}else{
						str = thisLine;
					}
					
					tidCount++;		
		        	
		        	 //////////////////////////////////////
		        	// writer.write(Double.toString(floatNumber)+", "+str +"\n");    //String.format("%.2f", f)
		        	 writer.write(str +"\n");
		        	 //////////////////////////////////////	                     	
		         }
		 		    writer.flush();
	 		}
	         
	     }catch(Exception e){
	    	 System.out.println(e.toString());
	     }		
	     

		//end try
	     System.out.println("change OK, tidCount: " + tidCount);	 
	     System.out.println("ratioOfNegativeItems: " + ratioOfNegativeItems +", "+ sizeOfItems*ratioOfNegativeItems);	 
	     System.out.println("negativeItems: " + negativeItems);	 
	     System.out.println("=====done!!=====");	
	

	}

}
