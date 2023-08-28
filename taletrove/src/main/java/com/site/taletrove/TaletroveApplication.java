package com.site.taletrove;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;

@SpringBootApplication(exclude = {SecurityAutoConfiguration.class})
public class TaletroveApplication {

	public static void main(String[] args) {
		SpringApplication.run(TaletroveApplication.class, args);
	}

}
