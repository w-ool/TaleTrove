package com.site.taletrove;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class TaletroveController {

    @GetMapping("/")
    public String index() {
        return "titlesearch";
    }

    @GetMapping("/recommend")
    public String recommend() {
        return "recommend";
    }

    @GetMapping("/info")
    public String info() {
        return "info";
    }

}