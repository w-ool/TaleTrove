package com.site.taletrove;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class TitleSearchController {
    @GetMapping("/index")
    public String titleSearch() {
        return "titleSearch";
    }
}
