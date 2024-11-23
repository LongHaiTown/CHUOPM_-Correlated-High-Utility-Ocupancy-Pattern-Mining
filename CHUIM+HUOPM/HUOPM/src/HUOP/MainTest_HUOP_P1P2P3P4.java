package HUOP;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

/**
 * Example of how to use the HUOP algorithm 
 * from the source code.
 * @author Wensheng Gan, HIT, IIIRC
 */
public class MainTest_HUOP_P1P2P3P4 {

	public static void main(String [] arg) throws IOException{
//		// T40I10D100K    kosarak_100K  T5I2N2KD100K    T10I4D100K  retail   BMS-WebView-1
		String input = "src/TestDatasets/1HUOP_New.txt";
		String utility_table_input = "src/TestDatasets/1HUOP_UtilityTable.txt";
		
//		String input = "src/TestDatasets/T10I4D100K_UM_New.txt";
//		String utility_t¤Îable_input = "src/TestDatasets/T10I4D100K_UM_UtilityTable.txt";
		String output = ".//output_HUOI.txt";

		//==============================
		double minSupport = 0.01;  // the minimum support threshold, (0,1]
		double minUtilOccu = 0.01;  // the minimum utility occupancy threshold, (0,1]
		int k=1;
		//==============================
		
		long SumTime =0;
		System.out.println("    ============  HUOP (P1 + P2 + P3 + P4) Algorithm !!! ============ " );
		System.out.println(" Dataset: " + input);
		System.out.println(" minSupport: " + String.format("%.6f", minSupport));
		System.out.println(" minUtilOccu: " + String.format("%.6f", minUtilOccu));

		for(int i=0; i<k; i++){
			//System.out.println(" ¡ñ¡ñ¡ñ¡ñ¡ñ¡ñ¡¾"+i+"¡¿¡ñ¡ñ¡ñ¡ñ¡ñ¡ñ ");
			// Applying the HUOP algorithm
			AlgoHUOP_P1P2P3P4 HUOP = new AlgoHUOP_P1P2P3P4();
			HUOP.runAlgorithm(input, utility_table_input, output, minSupport, minUtilOccu);
			HUOP.printStats();
			SumTime += HUOP.Time();
		}
		System.out.println("******average time: "+ SumTime/k/1000.0 + " s");

	}

	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = MainTest_HUOP_P1P2P3P4.class.getResource(filename);
		return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}
}