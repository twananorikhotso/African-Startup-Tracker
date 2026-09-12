package com.africa.backend.controller;

import com.africa.backend.entity.Startup;
import com.africa.backend.repository.StartupRepository;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(origins = "*")
@RequestMapping("/startups")
public class StartupController {

    private final StartupRepository startupRepository;

    public StartupController(StartupRepository startupRepository) {
        this.startupRepository = startupRepository;
    }

    @GetMapping
    public List<Startup> getAllStartups() {
        return startupRepository.findAll();
    }

    @PostMapping
    public Startup createStartup(@Valid @RequestBody Startup startup) {
        return startupRepository.save(startup);
    }
}