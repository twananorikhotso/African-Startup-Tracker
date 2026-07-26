package com.africa.backend;

import com.africa.backend.entity.Startup;
import com.africa.backend.repository.StartupRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class StartupDataInitializer implements CommandLineRunner {

    private final StartupRepository startupRepository;

    public StartupDataInitializer(StartupRepository startupRepository) {
        this.startupRepository = startupRepository;
    }

    @Override
    public void run(String... args) {
        if (startupRepository.count() > 0) {
            return;
        }

        List<Startup> sampleStartups = List.of(
                new Startup("Paystack", "Nigeria", "FinTech", 200000000),
                new Startup("Flutterwave", "Nigeria", "Payments", 170000000),
                new Startup("Andela", "Nigeria", "Talent", 180000000),
                new Startup("Chipper Cash", "Ghana", "FinTech", 150000000),
                new Startup("Jumia", "Kenya", "E-commerce", 260000000)
        );

        startupRepository.saveAll(sampleStartups);
    }
}
