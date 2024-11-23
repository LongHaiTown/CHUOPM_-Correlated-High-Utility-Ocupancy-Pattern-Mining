package TestDatasets;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.StringTokenizer;
import java.util.Random; //导入Random类 

public class ChangDataBase {
	static int tidCount = 0; 
	    
	public static void main(String[] args) {

	     try {
	    	// 讀取多個資料庫
	 		///////////////////////////////////////////////////////////////////////////////
	 		// batch 讀取的資料庫  /Data_convert/src/test1/transaction.txt
	    	final String[] filename1 = { "src/TestDatasets/kosarak_UM_New.txt"};  
	 		final String[] filename2 = { "src/TestDatasets/kos.txt"};  
	 		///////////////////////////////////////////////////////////////////////////////
	 		//kosarak_UM_New.txt

	 		for(int i=0; i < 1; i++){
//		    	 FileReader file = new FileReader("C:/data_change/transaction.txt");
//		         File fileWrite = new File("C:/data_change/1.txt");
		    	 FileReader file = new FileReader(filename1[i]);
		         File fileWrite = new File(filename2[i]);
		    	 BufferedReader bufferedreader = new BufferedReader(file);
		         BufferedWriter writer = new BufferedWriter(new FileWriter(fileWrite));
		         String thisLine;              

		         while (tidCount < 50000 && (thisLine = bufferedreader.readLine()) != null) {
			         //String str = "";
			         
					// split the transaction according to the : separator
					//String[] data = thisLine.split(", ");
//					for (int i1 = 0; i1 < data.length; i1 = i1 + 2) {
//						// get the probabililty
//						 double floatNumber = 0;
//			        	 while(floatNumber < 0.5){ // avoiding the zero
//			        		  floatNumber = Math.random();//获取一个浮点数(0-1);
//			        	 }
//			        	 String probability =String.format("%.2f", floatNumber);
//						
//			            // get the item
//			        	 if(i1 == 0){
//			        		 String temp_str = probability + ", " + data[i1 + 1];
//			        		 str = str + temp_str;
//			        	 }else{
//			        		 String temp_str = ", " + probability + ", " + data[i1 + 1];
//			        		 str = str + temp_str;
//			        	 }
//												
//					}
					
					//str = data[0] + ", " + data[1] + ", "+ String.valueOf((int)(Double.valueOf(data[1])*1.2));
					
					tidCount++;		
		        	
		        	 //////////////////////////////////////
		        	// writer.write(Double.toString(floatNumber)+", "+str +"\n");    //String.format("%.2f", f)
		        	 writer.write(thisLine +"\n");
		        	 //////////////////////////////////////	                     	
		         }
		 		    writer.flush();
	 		}
	         
	     }catch(Exception e){
	    	 System.out.println(e.toString());
	     }		
	     

		//end try
	     System.out.println("change OK, tidCount: "+ tidCount);	 
	     System.out.println("=====done!!=====");	
	

	}

}
