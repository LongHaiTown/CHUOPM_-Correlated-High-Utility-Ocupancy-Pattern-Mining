package HUOP;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


/**
 * This is an implementation of the "HUOP Algorithm" for mining high utility-occupancy patterns
 *  as described in the conference paper : <br/>
 * <br/>
 * 
 * Wensheng Gan, Jerry Chun-Wei Lin, et al. (2016). HUOP: Mining High Utility Occupancy Patterns. 
 * Proc. of EDBT 2017. pp. XX�CXX.
 * 
 * @see UO_List
 * @see Element
 * @author Wensheng Gan, HIT, IIIRC
 * @date 09-01-2016
 * 
 */
public class AlgoHUOP_P1P2 {
	Map<Integer,UO_List> map = new HashMap<>();
	// save the result k-itemsets
	int itemsets1 = 0;
	int itemsets2 = 0;
	int itemsets3 = 0;
	int itemsets4 = 0;
	int itemsets5 = 0;
	int itemsets6 = 0;
	int itemsets7 = 0;
	int itemsets8 = 0;
	int itemsets9 = 0;
	int itemsets10 = 0;
	int count_other = 0;

	// variable for statistics
	double maxMemory = 0; // the maximum memory usage
	long startTimestamp = 0; // the time the algorithm started
	long endTimestamp1 = 0; // the time the algorithm terminated
	long endTimestamp2 = 0; // the time the algorithm terminated
	
	public double minUtilityOccu;
	public double minSupport;
	public int VisitedNodeCount = 0;   // the nodes need to be construct utility-list
	public int HUOPCount = 0; // the number of HQP generated
	public int tid = 0; // the number of transactions
//	long totalUtility = 0; // use the long
	
	// record the profit of each 1-items
	HashMap<String, Double> mapItemToUtility; 

	// We create a map to store the transaction utility (tu) of each transaction
	Map<Integer, Double> mapOfTU;  
	
	// key: item   value: the support of this item
	Map<Integer, Integer> mapItemToSupport;
	
    final List<Double> list_topK = new ArrayList<Double>();
		
	// A map to store the transaction weighted utility occupancy (TWUO) of each item
//	Map<Integer, Double> mapItemToTWUO;
	
	BufferedWriter writer = null; // writer to write the output file
	String thisLine;

	// this class represent an item and its utility in a transaction
	class Pair {
		int item = 0;
		double utility = 0;
	}

	
	/**
	 * Default constructor
	 */
	public AlgoHUOP_P1P2() {
	}

	
	//Comparator, we define our MyComparator,
	//but not extends Comparator
	 class MyComparator implements Comparator<Double>{
	     public int compare(Double o1, Double o2) {
	         // if n1 < n2, return the positive value,
	    	 // if n1 > n2, return the negative value
	         // thus, we can get the descending order
	         if(o1 < o2) { 
	             return 1;
	         }else if(o1 > o2) {
	             return -1;
	         }else {
	             return 0;
	         }
	     }
	     
	 }
	
	 
	/**
	 * Run the algorithm
	 * 
	 * @param input
	 *            the input file path
	 * @param output
	 *            the output file path
	 * @param minUtilityOccu
	 *            the minimum utility threshold
	 * @throws IOException
	 *             exception if error while writing the file
	 */

	public void runAlgorithm(String input, String utility_table_input, String output,
			double minSupport_ratio, double utilOccu_ratio) throws IOException {
		// reset maximum
		maxMemory = 0;

		startTimestamp = System.currentTimeMillis();

		writer = new BufferedWriter(new FileWriter(output));

		// We create a map to store the utility of each item
		mapItemToUtility = new HashMap<String, Double>();
		
		// We create a map to store the tu of each transaction
		mapOfTU = new HashMap<Integer, Double>();
		// Map to store the support of each item
		mapItemToSupport = new HashMap<Integer, Integer>();
		
//		mapItemToTWU = new HashMap<Integer, Double>();
		
//		mapItemToTWUO = new HashMap<Integer, Double>();		
				
		// We scan the database a first time to calculate the TWU of each item.
		Load_utilityTable(utility_table_input);

		BufferedReader myInput = null;
		int TidCount = 0;
		
		try {

			// prepare the object for reading the file
			myInput = new BufferedReader(new InputStreamReader(new FileInputStream(new File(input))));
			// for each line (transaction) until the end of file
			while ((thisLine = myInput.readLine()) != null) {

				// if the line is a comment, is empty or is a kind of metadata
				if (thisLine.isEmpty() == true || thisLine.charAt(0) == '#' || thisLine.charAt(0) == '%' || thisLine.charAt(0) == '@') {
					continue;
				}
				
				// split the transaction according to the : separator
				String[] data = thisLine.split(", ");
				double tu = 0; // transaction utility
				
				for (int i = 0; i < data.length; i = i + 2) {
					double utilityOfItem = mapItemToUtility.get(data[i + 1]) * Integer.parseInt(data[i]);
					tu += utilityOfItem;
				}
						
				//totalUtility += tu;
				mapOfTU.put(TidCount, tu);
//				System.out.println(TidCount + " tu: "+ tmp_tu);
				// for each item, we add the transaction information for each item
				for (int i = 0; i < data.length; i = i + 2) {
					// convert item to integer
					Integer item1 = Integer.parseInt(data[i + 1]);
					/*****************  support order   ****************/				
					// update the current support of that item
					Integer sup = mapItemToSupport.get(item1);
					sup = (int) ((sup == null) ? 1 : sup + 1); 
					mapItemToSupport.put(item1, sup);					
					/*****************  support order   ****************/
					
					
					/*****************   TWU order   *******************/
//					// get the current TWU of that item
//					Double twu = mapItemToTWU.get(item1);
//					// add the utility of the item in the current transaction to
//					// its twu
//					twu = (twu == null) ? tu : twu + tu; 
//					mapItemToTWU.put(item1, twu);
					/*****************   TWU order   *******************/
					
					
					/*****************  TWUO order   **********************/
//					// get the current TWU of that item
//					Double TWUO = mapItemToTWUO.get(item1);
//					// add the wo(X,T_q) of the item in the current transaction to
//					// its TWUO
//					double uoOfTransaction = mapItemToUtility.get(data[i + 1]) * Integer.parseInt(data[i])/tu;
//					TWUO = (TWUO == null) ? uoOfTransaction : TWUO + uoOfTransaction; 
//					mapItemToTWUO.put(item1, TWUO);
					/*****************  TWUO order   **********************/				
					
				}
				TidCount++;
			}

		} catch (Exception e) {
			// catches exception if error while reading the input file
			e.printStackTrace();
		} finally {
			if (myInput != null) {
				myInput.close(); // close the file
			}
		}
		
		minSupport = minSupport_ratio;
		minUtilityOccu = utilOccu_ratio; // minUtilityOccu in the range (0,1]

		//System.out.println("totalUtility=" + totalUtility + "   minUtilityOccu=" + minUtilityOccu);

		// CREATE A LIST TO STORE THE UO-list OF ITEMS WITH TWU >=
		// MIN_utility.
		List<UO_List> listOfutilityLists = new ArrayList<UO_List>();
		// CREATE A MAP TO STORE THE UO-list FOR EACH ITEM.
		// Key : item Value : UO-list associated to that item
		Map<Integer, UO_List> mapItemToUOList = new HashMap<Integer, UO_List>();

		// For each item
		for (Integer item : mapItemToSupport.keySet()) {
			// if the item is promising (sup >= minSupport * TidCount)
			// early filtering the non-frequent 1-items
			if (mapItemToSupport.get(item) >= minSupport * TidCount) {
				// create an empty UO-list that we will fill later.
				UO_List uoList = new UO_List(item);
				mapItemToUOList.put(item, uoList);
				// add the item to the list of high TWU items
				listOfutilityLists.add(uoList);
				map.put(item,uoList);
				VisitedNodeCount++;
			}
			// System.out.println(item+"  sup= " + mapItemToSupport.get(item));
			// System.out.println(item+"  average UO= " + mapItemToTWUO.get(item)/mapItemToSupport.get(item));
		}
		
//		System.out.println("mapItemToSupport= " + mapItemToSupport);
//		System.out.println("mapItemToTWU= " + mapItemToTWU);
//		System.out.println("mapItemToTWUO= " + mapItemToTWUO);
		
		
		// SORT THE LIST OF HIGH TWU ITEMS IN ASCENDING ORDER 
		Collections.sort(listOfutilityLists, new Comparator<UO_List>() {
			public int compare(UO_List o1, UO_List o2) {
				// compare the TWU of the items
				return compareItems(o1.item, o2.item);
			}
		});

		// SECOND DATABASE PASS TO CONSTRUCT THE UO-listS
		// OF 1-ITEMSETS (promising items)
		try {
			// prepare object for reading the file
			myInput = new BufferedReader(new InputStreamReader(new FileInputStream(new File(input))));
			// variable to count the number of transaction

			// for each line (transaction) until the end of file
			while ((thisLine = myInput.readLine()) != null) {
				// if the line is a comment, is empty or is a
				// kind of metadata
				if (thisLine.isEmpty() == true || thisLine.charAt(0) == '#' || thisLine.charAt(0) == '%' || thisLine.charAt(0) == '@') {
					continue;
				}

				ArrayList<String> items = new ArrayList<String>();
				ArrayList<String> items_quantity = new ArrayList<String>();
				// System.out.println("thisLine=  "+thisLine);
				// split the transaction according to the : separator
				String[] data = thisLine.split(", ");

				for (int i = 0; i < data.length - 1; i = i + 2) {
					// String item = data[i+1].toString();
					items.add(data[i + 1]);
					items_quantity.add(data[i]);
				}		
				
				// Copy the transaction into lists but without items with non-frequent
				double rutil = 0;  // remaining utility

				// Create a list to store items
				List<Pair> revisedTransaction = new ArrayList<Pair>();
				// for each item
				for (int i = 0; i < items.size(); i++) {
					// / convert values to integers
					Pair pair = new Pair();
					pair.item = Integer.parseInt(items.get(i));
					pair.utility = Integer.parseInt(items_quantity.get(i)) * mapItemToUtility.get(items.get(i));
					// if the item has enough support
					if (mapItemToSupport.get(pair.item) >= minSupport * TidCount) {
						// add it
						revisedTransaction.add(pair);
						rutil += pair.utility; 						
					}
				}
				

				Collections.sort(revisedTransaction, new Comparator<Pair>() {
					public int compare(Pair o1, Pair o2) {
						return compareItems(o1.item, o2.item); 

					}
				});

				// ===========================================================
				// for each item left in the transaction
				for (Pair pair : revisedTransaction) {
					// subtract the utility of this item from the remaining utility
					rutil = rutil - pair.utility;
					
					// get the UO-list of this item
					UO_List UOListOfItem = mapItemToUOList.get(pair.item);

					// Add a new Element to the UO-list of this item
					// corresponding to this transaction
					Element element = new Element(tid, pair.utility/mapOfTU.get(tid), rutil/mapOfTU.get(tid));

					UOListOfItem.addElement(element); 
				}
				// ===========================================================
				tid++; // increase tid number for next transaction

			}
		} catch (Exception e) {
			// to catch error while reading the input file
			e.printStackTrace();
		} finally {
			if (myInput != null) {
				myInput.close();
			}
		}

		// check the memory usage
		checkMemory();

		// Test, for each item
		// for (UO_List Px : listOfutilityLists) {
		// 	System.out.println(Px.item+":sup= " +Px.support+", uo= "+Px.sumUO +",  uo/sup= "+Px.sumUO/Px.support+", ruo= "+Px.sumRUO+",  ruo/sup= "+Px.sumRUO/Px.support);
		// }

		endTimestamp1 = System.currentTimeMillis();

		// Print out I

		System.out.println("Sorted Item by ascending TWU ");
		for (UO_List uo_List : listOfutilityLists) {
			System.out.print(uo_List.item + " ");
		}
		System.out.println("");
		// Mine the database recursively
		HUOP_Miner(new int[0], null, listOfutilityLists, minUtilityOccu);

		// check the memory usage again and close the file.
		checkMemory();
		// close output file
		writer.close();
		// record end time
		endTimestamp2 = System.currentTimeMillis();
		System.out.println("=========  mining !!! =========  "+(endTimestamp2-endTimestamp1)/1000.0+"  s");
	}

	// ====================
	// Sub-procedure
	// ====================

	// utility Table
	public void Load_utilityTable(String utility_table_input) {
		try {
			// System.out.println("connectionTextFile - Load_utilityTable");
			String line;

			BufferedReader br = new BufferedReader(new FileReader(utility_table_input)); 
			while ((line = br.readLine()) != null) {
				String[] tmp = line.split(", "); // 
				String item = tmp[0]; // 
				double utility = Double.valueOf(tmp[1]); 
//				double utility = 1.0; // the special case of utilities are all 1.0 (CIKM, DOFRA algorithm)
				mapItemToUtility.put(item, utility); 
			}
			br.close(); 
		} catch (Exception e) {
			System.out.println("Error about loading the utility table... " + e.toString());
		}
	}

	
	/**
	 * Compare function, sort the items in each transaction
	 * 
	 * @param item1
	 * @param item2
	 * @return
	 */
	private int compareItems(int item1, int item2) {
		
		/*****************  lexical order   **********************/
//		return item1 - item2;
		/*****************  lexical order   **********************/
		
		
		/*****************  support ascending order   **********************/	
		int compare = mapItemToSupport.get(item1) - mapItemToSupport.get(item2);
		// if the same, use the lexical order otherwise use the support ascending order
		return (compare == 0) ? item1 - item2 : compare;
		/*****************  support ascending order   **********************/	
		
//		/*****************  support descending order   **********************/	
//		int compare = mapItemToSupport.get(item2) - mapItemToSupport.get(item1);
//		// if the same, use the lexical order otherwise use the support ascending order
//		return (compare == 0) ? item1 - item2 : compare;
//		/*****************  support descending order   **********************/	
		
		
		/*****************   TWU ascending order   ********************/	
//		int compare = (int)(mapItemToTWU.get(item1) - mapItemToTWU.get(item2));
//		// if the same, use the lexical order otherwise use the TWU
//		return (compare == 0) ? item1 - item2 : compare;
		/*****************   TWU ascending order   ********************/	
		
		
		/*****************   TWU descending order   ********************/	
//		int compare = (int)(mapItemToTWU.get(item2) - mapItemToTWU.get(item1));
//		// if the same, use the lexical order otherwise use the TWU
//		return (compare == 0) ? item1 - item2 : compare;
		/*****************   TWU descending order   ********************/	
		
		
		
		/*****************   TWUO ascending order   ********************/		
//		int compare =  (int) (mapItemToTWUO.get(item1) - mapItemToTWUO.get(item2));
//		// if the same, use the lexical order otherwise use the support ascending order
//		return (compare == 0) ? item1 - item2 : compare;
		/*****************   TWUO ascending order   ********************/
		
		
		/*****************   TWUO descending order   ********************/		
//		int compare =  (int) (mapItemToTWUO.get(item2) - mapItemToTWUO.get(item1));
//		// if the same, use the lexical order otherwise use the support ascending order
//		return (compare == 0) ? item1 - item2 : compare;
		/*****************   TWUO descending order   ********************/
		
		
		
		/*****************   average UO ascending order   ********************/		
//		Double o1 = mapItemToTWUO.get(item1)/mapItemToSupport.get(item1);
//		Double o2 = mapItemToTWUO.get(item2)/mapItemToSupport.get(item2);
//		if(o1 < o2) { 
//            return -1;
//        }else if(o1 > o2) {
//            return 1;
//        }else {
//            return 0;
//        }
		/*****************   average UO ascending order   ********************/
		
		
		
		/*****************   average UO descending order   ********************/		
//		Double o1 = mapItemToTWUO.get(item1)/mapItemToSupport.get(item1);
//		Double o2 = mapItemToTWUO.get(item2)/mapItemToSupport.get(item2);
//		if(o1 < o2) { 
//            return 1;
//        }else if(o1 > o2) {
//            return -1;
//        }else {
//            return 0;
//        }
		/*****************   average UO descending order   ********************/
	}

	
	
	/**
	 * This is the recursive method to find all high utility-occupancy itemsets. It writes
	 * the itemsets to the output file.
	 * 
	 * @param prefix
	 *            This is the current prefix. Initially, it is empty.
	 * @param pUL
	 *            This is the UO-list of the prefix. Initially, it is
	 *            empty.
	 * @param ULs
	 *            The UO-lists corresponding to each extension of the
	 *            prefix.
	 * @param minUtilityOccu
	 *            The minUtilityOccu threshold.
	 * @throws IOException
	 */
	private void HUOP_Miner(int[] prefix, UO_List pUL, List<UO_List> ULs, double minUtilityOccu) throws IOException {
		
		// For each extension X of prefix P
		for (int i = 0; i < ULs.size(); i++) {
			UO_List X = ULs.get(i);

			/********* Pruning strategy 1: support  **************/
			if(X.support >= (int) Math.ceil(minSupport * tid)){				
				// If pX is a high utility-occupancy itemset.
				// we save the itemset: pX				
				double occuOfX = X.getAvegUO();
				if (occuOfX >= minUtilityOccu) {
					// save to file
					writeOut(prefix, X.item, X.support, occuOfX);
					// checking the UOLx
					// if (prefix.length > 0){
					// 	StringBuffer buffer = new StringBuffer();
					// 	for (int j = 0; j < prefix.length; j++) {
					// 		buffer.append(prefix[j]);
					// 		buffer.append(' ');
					// 	}
					// 	System.out.println("------------");
					// 	System.out.print(buffer + "" +X.item);
					// 	X.showElement();
					// 	UO_List ulI = map.get(X.item);
					// 	System.out.println("-----" + X.item  + " " + ulI.elements.size());

					// 	for (int j = 0; j < prefix.length; j++) {
					// 		UO_List ulP = map.get(prefix[j]);
					// 		System.out.println("-----" + prefix[j]+ " " + ulP.elements.size());
					// 	}	
					// }else{
					// 	System.out.println("------------");
					// 	System.out.print(X.item);
					// 	X.showElement();
					// }
					
				}
				
				// If the upper-bound is higher than minUtilityOccu, we explore extensions of pX.
				// (this is the pruning condition)
				/********* Pruning strategy 2: upper bound *********/ 
				double maxOccuOfX = UpperBound(X);	
				if (maxOccuOfX >= minUtilityOccu) {
				
					// This list will contain the UO-lists of pX extensions.
					List<UO_List> exULs = new ArrayList<UO_List>();
					// =====================================================
					// For each extension of p appearing
					// after X according to the ascending order
					for (int j = i + 1; j < ULs.size(); j++) {
						UO_List Y = ULs.get(j);
						// we construct the extension pXY
						// and add it to the list of extensions of pX
						UO_List temp = construct(pUL, X, Y);
						
						/********* Pruning strategy 3: uo-list condition *********/
						if(temp != null && temp.support >= minSupport * tid) {
						   exULs.add(temp);
					    }
						
						VisitedNodeCount++;
					}
					
					// We create new prefix pX
					int[] newPrefix = new int[prefix.length + 1];
					System.arraycopy(prefix, 0, newPrefix, 0, prefix.length);
					/*
					 * System.arraycopy(src, srcPos, dest, destPos, length);					
					 */
					newPrefix[prefix.length] = X.item;
					// We make a recursive call to discover all itemsets with the prefix pX
					HUOP_Miner(newPrefix, X, exULs, minUtilityOccu); 
		
				}else{
			    	// System.out.println("P2..."+ X.item +"   maxOccuOfX="+ maxOccuOfX);
			    }
			}else{
		    	// System.out.println("P1..."+ X.item +"   sup="+ X.support);
		    }
			
		}
	}

	// ****************  Utility-Occupancy Counting **************
	/**
	 * Calculate the upper-bound 
	 * 
	 * @param ULOfX
	 * @return
	 */
	private double UpperBound(UO_List ULOfX) {
		// Note that we can not use: double[] topNValue = new double[(int) (minSupport * tid)];
		// the reason is that we can not know the top-k value until scan the whole ULOfX  
		Double[] topNValue = new Double[(int) (ULOfX.elements.size())];
		int transID = 0;
		double maxOccu = 0;
		
		for (Element ex : ULOfX.elements) {
			double occuInEachTid = ex.uo + ex.ruo; 
			topNValue[transID] = occuInEachTid;
			transID++;
		}

		// define MyComparator, descending order
		Arrays.sort(topNValue, new MyComparator());
		
		// select the top-k (minSupport * tid) value
		if((int) (minSupport * tid) == 0)
			return topNValue[0];
		else{
			// select the top-k (minSupport * tid) value
			for (int i = 0; i < (int) (minSupport * tid); i++) {
				maxOccu += topNValue[i];
//            System.out.println("maxOccu= "+ String.format("%.6f", minUtilityOccu) + "  ---"+topNValue[i]);
			}

			// use the average value of the summation
			return maxOccu/(int) (minSupport * tid);
		}
	}
	// ****************  Utility-Occupancy Counting **************
	

	/**
	 * This method constructs the UO-list of pXY �嫹
	 * 
	 * @param P
	 *            : the UO-list of prefix P.
	 * @param px
	 *            : the UO-list of pX
	 * @param py
	 *            : the UO-list of pY
	 * @return the UO-list of pXY
	 */
	private UO_List construct(UO_List P, UO_List px, UO_List py) {
		// create an empty UO-list for pXY
		UO_List pxyUL = new UO_List(py.item);
		
		// pruning strategy
//		int remainingSupport = px.support;
		
		// for each element in the UO-list of pX
		for (Element ex : px.elements) {
			// tid = ex.tid
			// do a binary search to find element ey in py with tid = ex.tid
			Element ey = findElementWithTID(py, ex.tid); // ****** 

			if (ey == null) {				
//				/*********  Pruning strategy 4  **********/
//				remainingSupport --;
//				if(remainingSupport < minSupport * tid) {
//					return null;
//				}
//				/*********  Pruning strategy 4  **********/
				
				continue;
			}
			
			// if the prefix p is null
			if (P == null) {
				// Create the new element
				// ============================================================================
				Element eXY = new Element(ex.tid, ex.uo + ey.uo, ey.ruo);
				// ============================================================================
				// add the new element to the UO-list of pXY
				pxyUL.addElement(eXY);

			} else {
				// find the element in the UO-list of p with the same tid
				Element e = findElementWithTID(P, ex.tid); // ****** ��
				if (e != null) {
					// Create new element
					// ============================================================================
					Element eXY = new Element(ex.tid, ex.uo + ey.uo - e.uo, ey.ruo);
					// ============================================================================
					// add the new element to the UO-list of pXY
					pxyUL.addElement(eXY);
				}
			}
		}
		// return the UO-list of pXY.
		return pxyUL;
	}

	/**
	 * Do a binary search to find the element with a given tid in a UO-list
	 * 
	 * @param ulist
	 *            : the UO-list
	 * @param tid
	 *            : the tid
	 * @return the element or null if none has the tid.
	 */
	private Element findElementWithTID(UO_List ulist, int tid) {
		List<Element> list = ulist.elements;

		// perform a binary search to check if the subset appears in level k-1.
		int first = 0;
		int last = list.size() - 1;

		// the binary search
		while (first <= last) {
			int middle = (first + last) >>> 1; // ???
	
			if (list.get(middle).tid < tid) {
				// the itemset compared is larger than the
				// subset according to the lexical order
				first = middle + 1; 
			} else if (list.get(middle).tid > tid) {
				// the itemset compared is smaller than the
				// subset is smaller according to the lexical order
				last = middle - 1; 	
			} else {
				return list.get(middle);
			}
		}
		return null;
	}

	/**
	 * Method to write a high utility-occupancy itemset to the output file.
	 * 
	 * @param the
	 *            prefix to be written o the output file
	 * @param an
	 *            item to be appended to the prefix
	 * @param utility
	 *            the utility of the prefix concatenated with the item
	 */
	private void writeOut(int[] prefix, int item, int sup, double uo) throws IOException {
		HUOPCount++; // increase the number of high utility-occupancy itemsets found

		if (prefix.length == 0) {
			itemsets1++;
		} else if (prefix.length == 1) {
			itemsets2++;
		} else if (prefix.length == 2) {
			itemsets3++;
		} else if (prefix.length == 3) {
			itemsets4++;
		} else if (prefix.length == 4) {
			itemsets5++;
		} else if (prefix.length == 5) {
			itemsets6++;
		} else if (prefix.length == 6) {
			itemsets7++;
		} else if (prefix.length == 7) {
			itemsets8++;
		} else if (prefix.length == 8) {
			itemsets9++;
		} else if (prefix.length == 9) {
			itemsets10++;
		} else {
			count_other++;
		}

		// Create a string buffer
		StringBuffer buffer = new StringBuffer();
		// append the prefix
		for (int i = 0; i < prefix.length; i++) {
			buffer.append(prefix[i]);
			buffer.append(' ');
		}
		// append the last item
		buffer.append(item);
		buffer.append(':');
		// append the support value
		buffer.append(" sup= " + sup);
		// append the utility-occupancy value
		buffer.append(", uo= " + String.format("%.6f", uo));
		
		// ***********  output **************
//		List<Double> list_topK = new ArrayList<Double>();
		if(list_topK.size() < 10) {
			list_topK.add(uo);
		}else {
			if(list_topK.get(0) < uo) {
				list_topK.remove(0);
				list_topK.add(uo);
			}
		}
		Collections.sort(list_topK);
		// ***********  output **************	
			

		// write to file
		writer.write(buffer.toString());
		writer.newLine();
	}

	/**
	 * Method to check the memory usage and keep the maximum memory usage.
	 */
	private void checkMemory() {
		// get the current memory usage
		double currentMemory = (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / 1024d / 1024d;
		// if higher than the maximum until now
		if (currentMemory > maxMemory) {
			// replace the maximum with the current memory usage
			maxMemory = currentMemory;
		}
	}

	/**
	 * Print statistics about the latest execution to System.out.
	 */
	public void printStats() {		
		System.out.println("=============  HUOP (P1 + P2) - STATS =============");
		System.out.println(" Total trans: " + tid);
		System.out.println(" min Support: " + String.format("%.2f", minSupport*tid));
		System.out.println(" min UtilityOccu: " + String.format("%.4f", minUtilityOccu));
		System.out.println(" Total time: " + (endTimestamp2 - startTimestamp)/1000.0 + " s");
		System.out.println(" Memory: " + String .format("%.2f", maxMemory) + " MB");
		System.out.println(" Visited nodes: " + VisitedNodeCount);
		System.out.println(" HUOPs: " + HUOPCount);
		System.out.println("=========================================");
		System.out.println(" 1-itemsets : " + itemsets1);
		System.out.println(" 2-itemsets : " + itemsets2);
		System.out.println(" 3-itemsets : " + itemsets3);
		System.out.println(" 4-itemsets : " + itemsets4);
		System.out.println(" 5-itemsets : " + itemsets5);
		System.out.println(" 6-itemsets : " + itemsets6);
		System.out.println(" 7-itemsets : " + itemsets7);
		System.out.println(" 8-itemsets : " + itemsets8);
		System.out.println(" 9-itemsets : " + itemsets9);
		System.out.println(" 10-itemsets : " + itemsets10);
		System.out.println(" count_other : " + count_other);
		System.out.println(" list_topK: " + list_topK);
	}

	public long Time() {
		 return (endTimestamp2 - startTimestamp);
	}
}