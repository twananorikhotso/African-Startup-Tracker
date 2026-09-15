package com.africa.backend.controller;

import com.africa.backend.entity.Startup;
import com.africa.backend.repository.StartupRepository;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin(origins = "*")
@RequestMapping("/startups")
public class StartupController {

    private static final Logger logger =
            LoggerFactory.getLogger(StartupController.class);

    private final StartupRepository startupRepository;

    public StartupController(StartupRepository startupRepository) {
        this.startupRepository = startupRepository;
    }

    @GetMapping
    public List<Startup> getAllStartups() {
        logger.info("Received request to retrieve all startups");

        List<Startup> startups = startupRepository.findAll();

        logger.info("Retrieved {} startups", startups.size());

        return startups;
    }

    @PostMapping
    public Startup createStartup(@Valid @RequestBody Startup startup) {
        logger.info(
                "Received request to create startup: {}",
                startup.getCompany()
        );

        Startup savedStartup = startupRepository.save(startup);

        logger.info(
                "Successfully created startup with ID: {}",
                savedStartup.getId()
        );

        return savedStartup;
    }
}