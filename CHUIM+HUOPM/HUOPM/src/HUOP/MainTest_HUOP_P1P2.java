package HUOP;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

/**
 * Example of how to use the HUOP algorithm 
 * from the source code.
 * @author Wensheng Gan, HIT, IIIRC
 */
public class MainTest_HUOP_P1P2 {

	public static void main(String [] arg) throws IOException{
		// T40I10D100K    kosarak_100K  T5I2N2KD100K    T10I4D100K  retail   BMS-WebView-1
//		String input = "src/TestDatasets/2DB_New.txt";  
//		String utility_table_input = "src/TestDatasets/2DB_UtilityTable.txt";  
		
		String input = "src/TestDatasets/2DB_New.txt";  
		String utility_table_input = "src/TestDatasets/2DB_UtilityTable.txt";  
		String output = ".//output_HUOI.txt";

		//==============================
		double minSupport = 0.011;  // the minimum support threshold, (0,1]
		double minUtilOccu = 0.3;  // the minimum utility occupancy threshold, (0,1]
		int k=1;
		//==============================
		
		long SumTime = 0;
		System.out.println("    ============  HUOP (P1 + P2) Algorithm !!! ============ " );
		System.out.println(" Dataset: " + input);
		System.out.println(" minSupport: " + String.format("%.6f", minSupport));
		System.out.println(" minUtilOccu: " + String.format("%.6f", minUtilOccu));

		for(int i=0; i<k; i++){
			//System.out.println(" �������"+i+"��������� ");
			// Applying the HUOP algorithm
			AlgoHUOP_P1P2 HUOP = new AlgoHUOP_P1P2();
			HUOP.runAlgorithm(input, utility_table_input, output, minSupport, minUtilOccu);
			HUOP.printStats();
			SumTime += HUOP.Time();
		}
		System.out.println("******average time: "+ SumTime/k/1000.0 + " s");

	}

	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = MainTest_HUOP_P1P2.class.getResource(filename);
		 return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}
}
