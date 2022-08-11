import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        String PATH = "driver/chromedriver";
        System.setProperty("webdriver.chrome.driver", PATH);
        WebDriver driver = new ChromeDriver();
        driver.manage().window().maximize();

        String url = "https://safetysigns.co.za/command-road-signs";
        driver.get(url);

        List<String> links0 = getLinks(driver);

        List<String> links1 = new ArrayList<>();
        for (String link : links0) {
            String imageLink = getImageLink(driver, link);
            if (imageLink != null && imageLink.contains("http")) {
                links1.add(imageLink);
            }
        }
        driver.close();

        downloadImages(links1);
        System.exit(0);
    }

    public static void downloadImages(List<String> links1){
        int i = 0;
        for (String link : links1) {
            downloadImage(link, i);
            i++;
        }
        System.out.println("Done");
    }
    public static void downloadImage(String imageUrl, int i) {
        try {
            URL imageURL = new URL(imageUrl);
            BufferedImage saveImage = ImageIO.read(imageURL);

            ImageIO.write(saveImage, "png", new File(String.format("command/%s.png", i)));
            System.out.println("Successful");
        }
        catch (Exception e) {
            System.out.println("Failed - " + e.getMessage());
            e.printStackTrace();
        }
    }

    public static String getImageLink(WebDriver driver, String url){
        driver.get(url);
        WebElement image = driver.findElement(By.xpath("/html/body/div[1]/div/div/div[3]/div[1]/div[1]/div[1]/a/img"));
        String link = image.getAttribute("src");
        if(link != null && link.contains("http")) {
            System.out.print("src: ");
            System.out.println(link);
            return link;
        }
        return null;
    }

    public static List<String> getLinks(WebDriver driver){
        List<String> links = new ArrayList<>();
        List<WebElement> divs = driver.findElements(By.className("image"));
        for (WebElement div : divs) {
            List<WebElement> as = div.findElements(By.tagName("a"));
            for (WebElement a : as) {
                String link = a.getAttribute("href");
                if(link != null && link.contains("http")) {
                    System.out.print("href: ");
                    System.out.println(link);
                    links.add(link);
                }
            }
        }
        return links;
    }
}
