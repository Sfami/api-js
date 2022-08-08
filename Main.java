package main;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.List;

import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.Alert;

public class MainProgram {
	

	public static void scrollDown(WebDriver driver) throws Exception {
		JavascriptExecutor js = (JavascriptExecutor) driver;
        //This will scroll the web page till end.		
        js.executeScript("window.scrollTo(0, document.body.scrollHeight)");
		Thread.sleep(300);

	}
	
	public static void downloadImage(String imageUrl) {
		try {
			URL imageURL = new URL(imageUrl);
	        BufferedImage saveImage = ImageIO.read(imageURL);
	          
	        ImageIO.write(saveImage, "png", new File("images/logo-forum.png"));
	        System.out.print("Successful");           
	    }
		catch (Exception e) {
			System.out.print("Failed - " + e.getMessage());  
			e.printStackTrace();
		}
	}
	
	public static void getImagesFromWeb(WebDriver driver, int numberOfImages) throws Exception {
		String url = "https://google.com";
		
		driver.get(url);
		driver.manage().window().maximize();
		
//		scrollDown(driver);
		
	    WebElement searchBar = driver.findElement(By.xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input"));
	    searchBar.sendKeys("stop sign png");
	    
	    WebElement searchBtn = driver.findElement(By.xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]"));
	    searchBtn.click();
	    
	    WebElement imagesTab = driver.findElement(By.xpath("/html/body/div[7]/div/div[4]/div/div[1]/div/div[1]/div/div[2]/a"));
	    imagesTab.click();
	    
	    String link = getImageLink(driver, "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img");

	    if(link.contains("http")) {
	    	driver.close();
	    	downloadImage(link);
	    }

	}
	
	public static String getImageLink(WebDriver driver, String imageXpath) throws Exception {
		
		 String imageLink = "";
		 Actions actions = new Actions(driver);
		 WebElement image = driver.findElement(By.xpath(imageXpath));
		 image.click();
		 Thread.sleep(15000);
		    
		 actions.contextClick(image).perform();
		 
		 WebElement bigImage = driver.findElement(By.xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img"));
		 String link = bigImage.getAttribute("src");
		 System.out.println(link);
		 if(link.contains("http")) {
		    System.out.println(link);
		    return link;
		 }
		 else {
			 int i = 2;
			 while (!imageLink.contains("http")) {
				 String xpath = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div[2]/div[1]/div[1]/span/div[1]/div[1]/div[%s]/a[1]/div[1]/img";
				 imageLink = getImageLink(driver, String.format(xpath, i));
			 }
			 
		 }
		 
		 return imageLink;
	
	}
	

	public static void main(String[] args) throws Exception {
		String PATH = "C:\\Users\\takal\\OneDrive\\Desktop\\Orifha\\Code\\Java\\chromedriver_win32\\";

		System.setProperty("webdriver.chrome.driver", PATH + "chromedriver.exe");
		WebDriver driver = new ChromeDriver();
	
		getImagesFromWeb(driver, 5);
		
	}
}
