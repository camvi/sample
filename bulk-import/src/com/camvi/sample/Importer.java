package com.camvi.sample;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;

import javax.imageio.ImageIO;

public class Importer extends ServerSession {

	public Importer() {
		super("http://localhost:8080/service/api", "admin", "admin");
		// super("http://192.168.56.101:8080/service/api", "admin", "admin");
	}
	
	public void importFromDirectory(String directory) {
		if (!loginSuccess()) {
			return;
		}
		
		System.out.println("Importing from : " + directory);
		int numThreads = Runtime.getRuntime().availableProcessors();
		ExecutorService threadPool = java.util.concurrent.Executors.newFixedThreadPool(numThreads);
		File[] files = new File(directory).listFiles();
		int numImported = 0;
	    for (File file : files) {
	        if (!file.isDirectory()) 
	        {
	        	System.out.println("Importing person : " + file.getName());
	        	threadPool.execute(new Runnable() {

					@Override
					public void run() {
						registerPerson(file.getName(), 1, file);
					}});
	        } 
	        numImported ++;
	    }
	    threadPool.shutdown();
	    System.out.println("Number of persons imported: " + numImported);
	}
	
	public void registerPerson(String userName, int groupId, File imageFile)
    {
        Map<String, String> params = new HashMap<String, String>();
        params.put("person-name", userName);
        params.put("group-ids", Integer.toString(groupId));
        if (serverBase.indexOf("localhost") >= 0) {
        	// file is local
        	params.put("server-image-file", imageFile.getName());
        } else {
        	// file is remote
            BufferedImage img;
            try {
            	img = ImageIO.read(imageFile);
            } catch (IOException e) {
    			// TODO Auto-generated catch block
    			e.printStackTrace();
    			return;
    		}
            if (img == null) {
            	System.out.println("Unable to read image from "+imageFile.getName());
            	return;
            }
            params.put("image-data", toBase64Image(img));
        }

        try {
            String resp = new String(doPost("/person/create", params));
            System.out.println("RESULT: " + resp);
        } catch (Exception e) {
            System.out.println("Error registerPerson: " + e.getMessage());
            e.printStackTrace();
        }
    }
	
	public static void main(String[] args) {
		if (args.length < 1) {
			System.out.println("Argument: <import directory>");
			System.out.println("Example: /path/to/import");
			return;
		}
		Importer importer = new Importer();
		importer.importFromDirectory(args[0]);
	}
}
